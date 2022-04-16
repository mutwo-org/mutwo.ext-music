from __future__ import annotations

import numbers
import operator
import typing
import warnings

try:
    import quicktions as fractions  # type: ignore
except ImportError:
    import fractions  # type: ignore

from mutwo import core_constants
from mutwo import core_utilities
from mutwo import music_parameters

from .EqualDividedOctavePitch import EqualDividedOctavePitch


__all__ = ("WesternPitch",)

ConcertPitch = typing.Union[core_constants.Real, music_parameters.abc.Pitch]
PitchClassOrPitchClassName = typing.Union[core_constants.Real, str]


class WesternPitch(EqualDividedOctavePitch):
    """Pitch with a traditional Western nomenclature.

    :param pitch_class_or_pitch_class_name: Name or number of the pitch
        class of the new ``WesternPitch`` object. The nomenclature is
        English (c, d, e, f, g, a, b). It uses an equal divided octave
        system in 12 chromatic steps. Accidentals are indicated by
        (s = sharp) and (f = flat). Further microtonal accidentals are
        supported (see
        :const:`mutwo.music_parameters.configurations.ACCIDENTAL_NAME_TO_PITCH_CLASS_MODIFICATION_DICT`
        for all supported accidentals).
    :type pitch_class_or_pitch_class_name: PitchClassOrPitchClassName
    :param octave: The octave of the new :class:`WesternPitch` object.
        Indications for the specific octave follow the MIDI Standard where
        4 is defined as one line.
    :type octave: int

    **Example:**

    >>> from mutwo.music_parameters import pitches
    >>> pitches.WesternPitch('cs', 4)  # c-sharp 4
    >>> pitches.WesternPitch('aqs', 2)  # a-quarter-sharp 2
    """

    def __init__(
        self,
        pitch_class_or_pitch_class_name: PitchClassOrPitchClassName = 0,
        octave: int = 4,
        concert_pitch_pitch_class: core_constants.Real = None,
        concert_pitch_octave: int = None,
        concert_pitch: ConcertPitch = None,
        *args,
        **kwargs,
    ):
        if concert_pitch_pitch_class is None:
            concert_pitch_pitch_class = (
                music_parameters.configurations.DEFAULT_CONCERT_PITCH_PITCH_CLASS_FOR_WESTERN_PITCH
            )

        if concert_pitch_octave is None:
            concert_pitch_octave = (
                music_parameters.configurations.DEFAULT_CONCERT_PITCH_OCTAVE_FOR_WESTERN_PITCH
            )

        (
            pitch_class,
            pitch_class_name,
        ) = self._pitch_class_or_pitch_class_name_to_pitch_class_and_pitch_class_name(
            pitch_class_or_pitch_class_name
        )

        super().__init__(
            music_parameters.constants.CHROMATIC_PITCH_CLASS_COUNT,
            pitch_class,
            octave,
            concert_pitch_pitch_class,
            concert_pitch_octave,
            concert_pitch,
            *args,
            **kwargs,
        )

        self._pitch_class_name = pitch_class_name

    # ###################################################################### #
    #                      static private methods                            #
    # ###################################################################### #

    @staticmethod
    def _pitch_class_or_pitch_class_name_to_pitch_class_and_pitch_class_name(
        pitch_class_or_pitch_class_name: PitchClassOrPitchClassName,
    ) -> tuple:
        """Helper function to initialise a WesternPitch from a number or a string.

        A number has to represent the pitch class while the name has to use
        the Western English nomenclature with the form
        DIATONICPITCHCLASSNAME-ACCIDENTAL (e.g. "cs" for c-sharp,
        "gqf" for g-quarter-flat, "b" for b)
        """
        if isinstance(pitch_class_or_pitch_class_name, numbers.Real):
            pitch_class = float(pitch_class_or_pitch_class_name)
            pitch_class_name = WesternPitch._pitch_class_to_pitch_class_name(
                pitch_class_or_pitch_class_name
            )
        elif isinstance(pitch_class_or_pitch_class_name, str):
            pitch_class = WesternPitch._pitch_class_name_to_pitch_class(
                pitch_class_or_pitch_class_name
            )
            pitch_class_name = pitch_class_or_pitch_class_name
        else:
            raise TypeError(
                "Can't initalise pitch_class by "
                f"'{pitch_class_or_pitch_class_name}' of type"
                f" '{type(pitch_class_or_pitch_class_name)}'."
            )

        return pitch_class, pitch_class_name

    @staticmethod
    def _accidental_to_pitch_class_modifications(
        accidental: str,
    ) -> core_constants.Real:
        """Helper function to translate an accidental to its pitch class modification.

        Raises an error if the accidental hasn't been defined yet in
        mutwo.music_parameters.configurations.ACCIDENTAL_NAME_TO_PITCH_CLASS_MODIFICATION_DICT.
        """
        try:
            return music_parameters.configurations.ACCIDENTAL_NAME_TO_PITCH_CLASS_MODIFICATION_DICT[
                accidental
            ]
        except KeyError:
            raise NotImplementedError(
                "Can't initialise WesternPitch with "
                f"unknown accidental {accidental}! Please see "
                "'music_parameters.configurations.ACCIDENTAL_NAME_TO_PITCH_CLASS_MODIFICATION_DICT'"
                " for a list of allowed accidentals."
            )

    @staticmethod
    def _pitch_class_name_to_pitch_class(
        pitch_class_name: str,
    ) -> float:
        """Helper function to translate a pitch class name to its respective number.

        +/-1 is defined as one chromatic step. Smaller floating point numbers
        represent microtonal inflections..
        """
        diatonic_pitch_class_name, accidental = (
            pitch_class_name[0],
            pitch_class_name[1:],
        )
        diatonic_pitch_class = (
            music_parameters.constants.DIATONIC_PITCH_NAME_TO_PITCH_CLASS_DICT[
                diatonic_pitch_class_name
            ]
        )
        pitch_class_modification = (
            WesternPitch._accidental_to_pitch_class_modifications(accidental)
        )
        return float(diatonic_pitch_class + pitch_class_modification)

    @staticmethod
    def _difference_to_closest_diatonic_pitch_to_accidental(
        difference_to_closest_diatonic_pitch: core_constants.Real,
    ) -> str:
        """Helper function to translate a number to the closest known accidental."""

        closest_pitch_class_modification: fractions.Fraction = core_utilities.find_closest_item(
            difference_to_closest_diatonic_pitch,
            tuple(
                music_parameters.configurations.PITCH_CLASS_MODIFICATION_TO_ACCIDENTAL_NAME_DICT.keys()
            ),
        )
        closest_accidental = music_parameters.configurations.PITCH_CLASS_MODIFICATION_TO_ACCIDENTAL_NAME_DICT[
            closest_pitch_class_modification
        ]
        return closest_accidental

    @staticmethod
    def _pitch_class_to_pitch_class_name(
        pitch_class: core_constants.Real,
    ) -> str:
        """Helper function to translate a pitch class in number to a string.

        The returned pitch class name uses a Western nomenclature of English
        diatonic note names. Accidental names are defined in
        mutwo.music_parameters.configurations.ACCIDENTAL_NAME_TO_PITCH_CLASS_MODIFICATION_DICT.
        For floating point numbers the closest accidental is chosen.
        """
        diatonic_pitch_classes = tuple(
            music_parameters.constants.DIATONIC_PITCH_NAME_TO_PITCH_CLASS_DICT.values()
        )
        closest_diatonic_pitch_class_index = core_utilities.find_closest_index(
            pitch_class, diatonic_pitch_classes
        )
        diatonic_pitch_class = diatonic_pitch_classes[
            closest_diatonic_pitch_class_index
        ]
        diatonic_pitch = tuple(
            music_parameters.constants.DIATONIC_PITCH_NAME_TO_PITCH_CLASS_DICT.keys()
        )[closest_diatonic_pitch_class_index]

        accidental_adjustments = pitch_class - diatonic_pitch_class

        accidental = WesternPitch._difference_to_closest_diatonic_pitch_to_accidental(
            accidental_adjustments
        )

        pitch_class_name = f"{diatonic_pitch}{accidental}"
        return pitch_class_name

    # ###################################################################### #
    #                      public class  methods                             #
    # ###################################################################### #

    @classmethod
    def from_midi_pitch_number(cls, midi_pitch_number: float) -> WesternPitch:
        pitch_number = (
            midi_pitch_number - music_parameters.constants.CHROMATIC_PITCH_CLASS_COUNT
        )
        pitch_class_number = (
            pitch_number % music_parameters.constants.CHROMATIC_PITCH_CLASS_COUNT
        )
        octave_number = int(
            pitch_number // music_parameters.constants.CHROMATIC_PITCH_CLASS_COUNT
        )
        return cls(pitch_class_number, octave=octave_number)

    # ###################################################################### #
    #                          magic methods                                 #
    # ###################################################################### #

    def __repr__(self) -> str:
        return f"{type(self).__name__}('{self.pitch_class_name}', {self.octave})"

    def __str__(self) -> str:
        return repr(self)

    # ###################################################################### #
    #                         private methods                                #
    # ###################################################################### #

    def _parse_pitch_interval(
        self,
        pitch_interval: typing.Union[
            str, music_parameters.abc.PitchInterval, core_constants.Real
        ],
    ) -> typing.Union[
        music_parameters.abc.PitchInterval,
        core_constants.Real,
        music_parameters.abc.PitchInterval,
    ]:
        if isinstance(pitch_interval, str):
            pitch_interval = music_parameters.WesternPitchInterval(pitch_interval)
        elif isinstance(pitch_interval, core_constants.Real.__args__ + (int,)):
            # Only convert to western pitch interval in case the interval isn't
            # microtonal (because WesternPitchInterval doesn't support
            # microtonality). 0.001 (= 0.1 cents) are set in case for
            # floating point errors.
            if abs(round(pitch_interval) - pitch_interval) < 0.001:
                pitch_interval = music_parameters.WesternPitchInterval(pitch_interval)
        return pitch_interval

    def _western_pitch_interval_to_operator(
        self, western_pitch_interval: music_parameters.WesternPitchInterval
    ) -> typing.Callable:
        return (operator.add, operator.sub)[western_pitch_interval.is_interval_falling]

    def _get_new_diatonic_pitch_class_name_and_octave_count(
        self, western_pitch_interval_to_add: music_parameters.WesternPitchInterval
    ) -> tuple[str, int]:
        current_diatonic_pitch_class_name_index = (
            music_parameters.constants.ASCENDING_DIATONIC_PITCH_NAME_TUPLE.index(
                self.diatonic_pitch_class_name
            )
        )
        diatonic_pitch_class_name_index_difference = (
            int(western_pitch_interval_to_add.interval_type) - 1
        )
        absolute_new_diatonic_pitch_class_name_index = (
            self._western_pitch_interval_to_operator(western_pitch_interval_to_add)(
                current_diatonic_pitch_class_name_index,
                diatonic_pitch_class_name_index_difference,
            )
        )
        new_diatonic_pitch_class_name_index = (
            absolute_new_diatonic_pitch_class_name_index
            % music_parameters.constants.DIATONIC_PITCH_CLASS_COUNT
        )
        octave_count = (
            absolute_new_diatonic_pitch_class_name_index
            // music_parameters.constants.DIATONIC_PITCH_CLASS_COUNT
        )

        new_diatonic_pitch_class_name = (
            music_parameters.constants.ASCENDING_DIATONIC_PITCH_NAME_TUPLE[
                new_diatonic_pitch_class_name_index
            ]
        )

        return new_diatonic_pitch_class_name, octave_count

    def _get_new_pitch_class_modification(
        self,
        western_pitch_interval_to_add: music_parameters.WesternPitchInterval,
        new_diatonic_pitch_class_name: str,
    ) -> fractions.Fraction:

        key = (self.diatonic_pitch_class_name, new_diatonic_pitch_class_name)
        if western_pitch_interval_to_add.is_interval_falling:
            key = tuple(reversed(key))

        added_cent_deviation = (
            western_pitch_interval_to_add.interval_quality_cent_deviation
            + music_parameters.constants.DIATONIC_PITCH_CLASS_NAME_PAIR_TO_COMPENSATION_IN_CENTS_DICT[
                key
            ]
        )
        added_pitch_class_modification = fractions.Fraction(
            int(added_cent_deviation),
            # 100 for cents -> to semitones
            100,
        )

        pitch_class_modification = self._western_pitch_interval_to_operator(
            western_pitch_interval_to_add
        )(
            music_parameters.configurations.ACCIDENTAL_NAME_TO_PITCH_CLASS_MODIFICATION_DICT[
                self.accidental_name
            ],
            added_pitch_class_modification,
        )
        return pitch_class_modification

    def _add_western_pitch_interval(
        self, western_pitch_interval_to_add: music_parameters.WesternPitchInterval
    ):
        (
            new_diatonic_pitch_class_name,
            octave_count,
        ) = self._get_new_diatonic_pitch_class_name_and_octave_count(
            western_pitch_interval_to_add
        )
        new_pitch_class_modification = self._get_new_pitch_class_modification(
            western_pitch_interval_to_add, new_diatonic_pitch_class_name
        )

        try:
            new_accidental = music_parameters.configurations.PITCH_CLASS_MODIFICATION_TO_ACCIDENTAL_NAME_DICT[
                new_pitch_class_modification
            ]
        except KeyError:
            # Fall back to default calculation (because the needed accidental
            # doesn't exist. We would need something even more sharp than
            # double sharp or even more flat than double flat).
            warnings.warn(
                "Couldn't get correct western pitch with "
                f"interval '{western_pitch_interval_to_add} to"
                f" '{self}'; pitch_modifiation: "
                f"{new_pitch_class_modification}.",
                RuntimeWarning,
            )
            return super().add(western_pitch_interval_to_add)

        new_pitch_class_name = f"{new_diatonic_pitch_class_name}{new_accidental}"

        self.pitch_class_name = new_pitch_class_name
        self.octave += octave_count

    # ###################################################################### #
    #                          public properties                             #
    # ###################################################################### #

    @property
    def name(self) -> str:
        """The name of the pitch in Western nomenclature."""

        return f"{self._pitch_class_name}{self.octave}"

    @property
    def pitch_class_name(self) -> str:
        """The name of the pitch class in Western nomenclature.

        Mutwo uses the English nomenclature for pitch class names:
            (c, d, e, f, g, a, b)
        """

        return self._pitch_class_name

    @pitch_class_name.setter
    def pitch_class_name(self, pitch_class_name: str):
        self._pitch_class = self._pitch_class_name_to_pitch_class(pitch_class_name)
        self._pitch_class_name = pitch_class_name

    @EqualDividedOctavePitch.pitch_class.setter  # type: ignore
    def pitch_class(self, pitch_class: core_constants.Real):
        self._pitch_class_name = self._pitch_class_to_pitch_class_name(pitch_class)
        self._pitch_class = pitch_class

    @property
    def diatonic_pitch_class_name(self) -> str:
        """Only get the diatonic part of the pitch name"""

        return self.pitch_class_name[0]

    @property
    def accidental_name(self) -> str:
        """Only get accidental part of pitch name"""

        return self.pitch_class_name[1:]

    @property
    def is_microtonal(self) -> bool:
        """Return `True` if accidental isn't on chromatic grid."""

        pitch_modifiation = music_parameters.configurations.ACCIDENTAL_NAME_TO_PITCH_CLASS_MODIFICATION_DICT[
            self.accidental_name
        ]
        return pitch_modifiation % fractions.Fraction(1, 1) != 0

    # ###################################################################### #
    #                          public methods                                #
    # ###################################################################### #

    @core_utilities.add_copy_option
    def add(  # type: ignore
        self,
        pitch_interval: typing.Union[
            str, music_parameters.abc.PitchInterval, core_constants.Real
        ],
    ) -> WesternPitch:  # type: ignore
        pitch_interval = self._parse_pitch_interval(pitch_interval)
        if isinstance(pitch_interval, music_parameters.WesternPitchInterval):
            self._add_western_pitch_interval(pitch_interval)
        else:
            return super().add(pitch_interval)  # type: ignore

    @core_utilities.add_copy_option
    def subtract(  # type: ignore
        self,
        pitch_interval: typing.Union[
            str, music_parameters.abc.PitchInterval, core_constants.Real
        ],
    ) -> WesternPitch:  # type: ignore
        pitch_interval = self._parse_pitch_interval(pitch_interval)
        if isinstance(pitch_interval, music_parameters.WesternPitchInterval):
            return self.add(pitch_interval.inverse_direction(mutate=False))
        else:
            return super().subtract(pitch_interval)  # type: ignore