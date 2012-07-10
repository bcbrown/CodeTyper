import unittest
import typer
from nltk.metrics import edit_distance

class TestLine(unittest.TestCase):

    def setUp(self):
        # These tests were written when I had my own edit distance algorithm
        # Now I'm using edit_distance, so bind it to the method called by the tests
        typer.evaluate_line = edit_distance
    
    def testAccurate(self):
        master = "here's some very simple text with no typos"
        self.assertEqual(typer.evaluate_line(master, master), 0)

    def testTypo(self):
        master = "this text is speedy!"
        sub = "this test is speedy!"
        self.assertEqual(typer.evaluate_line(master, sub), 1)

    def testSkipped(self):
        master = "who grew two blue shoes for you?"
        sub = "who grew two blue shoes fr you?"
        self.assertEqual(typer.evaluate_line(master, sub), 1)

    def testDoubleType(self):
        master = "Forever new, the sky glows with abandon"
        sub = "Forever neww, the sky glows with abandon"
        self.assertEqual(typer.evaluate_line(master, sub), 1)

    def testSeveralTypos(self):
        master = "Once again we find ourselves in Spain"
        sub = "One againwe find ourselves in spain"
        self.assertEqual(typer.evaluate_line(master, sub), 3)

    def testTooLong(self):
        master = "don't believe everything you think"
        sub = "don't believe everything you think, buddy"
        self.assertEqual(typer.evaluate_line(master, sub), 7)

    def testTooShort(self):
        master = "Authorities seldom signify sacrilege"
        sub = "Authorities seldom signify"
        self.assertEqual(typer.evaluate_line(master, sub), 10)

    def testDoubleTypo(self):
        master = "Too many pennies in Heaven"
        sub = "Too many ol[pennies in Heaven"
        self.assertEqual(typer.evaluate_line(master, sub), 3)

    def testBothEmpty(self):
        master = ""
        self.assertEqual(typer.evaluate_line(master, master), 0)
        
    def testTest(self):
        master = "123456789  "
        sub = "123456654 "
        self.assertEqual(typer.evaluate_line(master, master), 0)

    def testEmptyMaster(self):
        master = ""
        submission = "furtive"
        self.assertEqual(typer.evaluate_line(master, submission), 7)

    def testEmptySubmission(self):
        master = "not empty"
        sub = ""
        self.assertEqual(typer.evaluate_line(master, sub), 9)
        
    def testGreedyAlgorithmFailure(self):
        # My custom-written algorithm failed this test
        # Levenshtein distance passes this test
        master = "this text has spaces"
        sub = "        this text has spaces"
        self.assertEqual(typer.evaluate_line(master, sub), 8)

class TestParagraph(unittest.TestCase):
    def test_too_few_lines(self):
        master = []
        master.append("formal mornings of languid lounging")
        master.append("dissolute soldiers decry indecency")
        master.append("sesquipedalian")
		# the error is 15 because the missing '\n' is counted
        self.assertEqual(typer.evaluate_submission(master, master[:2]), 15)

    def test_too_many_lines(self):
        master = []
        master.append('felicitous formalisms frolic')
        master.append('derelict dirigibles drifting')
        master.append('artifactant')
		# the error is 12 because the missing '\n' is counted
        self.assertEqual(typer.evaluate_submission(master[:2], master), 12)

    def test_correct_lines(self):
        master = []
        master.append('uncontrollable appendages abound')
        master.append('journalistic intensity')
        self.assertEqual(typer.evaluate_submission(master, master), 0)

    def test_multi_line_errors(self):
        master = []
        master.append('against everything with intent')
        master.append('Hungarian lunches for everyone')
        master.append('a stubborn savage certainty')
        submission = []
        submission.append('against everythig with inten')# 2 typoes
        submission.append('huhngarin lunche for Everyon')# 6 typoes
        submission.append('a stubborn savage certaintyy')# 1 typo
        self.assertEqual(typer.evaluate_submission(master, submission), 9)

if __name__ == '__main__':
    unittest.main()