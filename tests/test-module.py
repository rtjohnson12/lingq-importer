import unittest
from unittest.mock import patch
from run import run


class TestRun(unittest.TestCase):
    @patch("src.lingq.get_courses_by_language")
    @patch("src.youtube.Channel")
    def test_run(self, mock_channel, mock_get_courses):
        # Mocking the necessary dependencies
        mock_channel.return_value = "mock_channel_instance"
        mock_get_courses.return_value = {"results": ["course1", "course2"]}

        # Running the function with test inputs
        run(
            channel_name="JorgeDeLeonMx",
            language_code="es",
            n_videos=50,
            manual_transcripts_only=True,
        )

        # Asserting the expected calls and outputs
        mock_channel.assert_called_once_with(
            "https://www.youtube.com/@JorgeDeLeonMx/videos"
        )
        mock_get_courses.assert_called_once_with(language_code="es")
        # Add more assertions as needed


if __name__ == "__main__":
    unittest.main()
