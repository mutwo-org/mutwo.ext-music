import unittest

try:
    import quicktions as fractions  # type: ignore
except ImportError:
    import fractions  # type: ignore

from mutwo.core.events import basic

from mutwo.ext.events import music
from mutwo.ext.parameters import pitches
from mutwo.ext.parameters import volumes


class NoteLikeTest(unittest.TestCase):
    # ###################################################################### #
    #                          test pitch setter                             #
    # ###################################################################### #

    def test_pitch_list_setter_from_string(self):
        self.assertEqual(
            [pitches.WesternPitch("ds", octave=5)],
            music.NoteLike("ds5", 1, 1).pitch_list,
        )
        self.assertEqual(
            [pitches.WesternPitch("f")],
            music.NoteLike("f", 1, 1).pitch_list,
        )
        self.assertEqual(
            [
                pitches.WesternPitch("f"),
                pitches.WesternPitch("g", 2),
                pitches.WesternPitch("af"),
            ],
            music.NoteLike("f g2 af", 1, 1).pitch_list,
        )
        self.assertEqual(
            [pitches.JustIntonationPitch("3/2")],
            music.NoteLike("3/2", 1, 1).pitch_list,
        )
        self.assertEqual(
            [pitches.JustIntonationPitch("11/1")],
            music.NoteLike("11/1", 1, 1).pitch_list,
        )
        self.assertEqual(
            [pitches.JustIntonationPitch("5/3"), pitches.WesternPitch("aqs", 5)],
            music.NoteLike("5/3 aqs5", 1, 1).pitch_list,
        )

    def test_pitch_list_setter_from_fraction(self):
        ratio = fractions.Fraction(3, 2)
        self.assertEqual(
            [pitches.JustIntonationPitch(ratio)],
            music.NoteLike(ratio, 1, 1).pitch_list,
        )

    def test_pitch_list_setter_from_None(self):
        self.assertEqual([], music.NoteLike(None, 1, 1).pitch_list)

    def test_pitch_list_setter_from_pitch(self):
        pitch_list = pitches.WesternPitch()
        self.assertEqual([pitch_list], music.NoteLike(pitch_list, 1, 1).pitch_list)

    def test_pitch_list_setter_from_list(self):
        pitch_list = [pitches.WesternPitch(), pitches.JustIntonationPitch()]
        self.assertEqual(pitch_list, music.NoteLike(pitch_list, 1, 1).pitch_list)

    # ###################################################################### #
    #                          test volume setter                            #
    # ###################################################################### #

    def test_volume_setter_from_volume(self):
        volume = volumes.DecibelVolume(-6)
        self.assertEqual(volume, music.NoteLike(None, 1, volume).volume)

    def test_volume_setter_from_positive_number(self):
        amplitude = 0.5
        volume = volumes.DirectVolume(amplitude)
        self.assertEqual(volume, music.NoteLike(None, 1, amplitude).volume)

    def test_volume_setter_from_negative_number(self):
        n_decibel = -12
        volume = volumes.DecibelVolume(n_decibel)
        self.assertEqual(volume, music.NoteLike(None, 1, n_decibel).volume)

    # ###################################################################### #
    #                   test grace notes setter                              #
    # ###################################################################### #

    def test_grace_note_sequential_event_setter_from_simple_event(self):
        grace_note_sequential_event = music.NoteLike()
        self.assertEqual(
            basic.SequentialEvent([grace_note_sequential_event]),
            music.NoteLike(
                None, 1, 1, grace_note_sequential_event
            ).grace_note_sequential_event,
        )

    def test_grace_note_sequential_event_setter_from_sequential_event(self):
        grace_note_sequential_event = basic.SequentialEvent([music.NoteLike()])
        self.assertEqual(
            grace_note_sequential_event,
            music.NoteLike(
                None, 1, 1, basic.SequentialEvent([]), grace_note_sequential_event
            ).after_grace_note_sequential_event,
        )

    # ###################################################################### #
    #                          other                                         #
    # ###################################################################### #

    def test_parameter_to_compare_tuple(self):
        note_like = music.NoteLike([pitches.WesternPitch()], 1, 1)
        expected_parameter_to_compare_tuple = (
            "after_grace_note_sequential_event",
            "duration",
            "grace_note_sequential_event",
            "notation_indicator_collection",
            "pitch_list",
            "playing_indicator_collection",
            "volume",
        )
        self.assertEqual(
            note_like._parameter_to_compare_tuple, expected_parameter_to_compare_tuple
        )

    def test_equality_check(self):
        note_like0 = music.NoteLike([30], 1, 1)
        note_like1 = music.NoteLike([30], 1, 1)
        note_like2 = music.NoteLike([100], 1, 1)
        note_like3 = music.NoteLike([], 1, 2)
        note_like4 = music.NoteLike([400, 500], 1, 2)
        simple_event = basic.SimpleEvent(1)

        self.assertEqual(note_like0, note_like0)
        self.assertEqual(note_like1, note_like0)
        self.assertEqual(note_like0, note_like1)  # different order

        self.assertNotEqual(note_like0, note_like2)
        self.assertNotEqual(note_like2, note_like0)  # different order
        self.assertNotEqual(note_like2, note_like3)
        self.assertNotEqual(note_like2, note_like4)
        self.assertNotEqual(note_like3, note_like4)
        self.assertNotEqual(note_like0, simple_event)
        self.assertNotEqual(simple_event, note_like0)  # different order
