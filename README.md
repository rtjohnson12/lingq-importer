# lingq-importer

`lingq-importer` is a Python project that allows you to import lessons/content from YouTube to LingQ. It provides a convenient way to automate the process of importing YouTube videos as lessons into your LingQ account.

## Features

- Fetches YouTube video details such as title, description, and captions.
- Converts YouTube captions to LingQ lesson format.
- Imports YouTube videos as lessons into your LingQ account.

## Prerequisites

Before using lingq-importer, make sure you have the following:

- Python 3 installed on your system.
- The `pip` package manager installed.

## Installation

1. Clone the repository:

```bash
git clone https://github.com/your-username/lingq-importer.git
```

2. Navigate to the project directory:

```bash
cd lingq-importer
```

3. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Configuration

To use lingq-importer, you need to provide your LingQ API key. Follow these steps to obtain your API key:

1. Go to https://www.lingq.com/en/accounts/apikey/
2. Create a file named .env in the project directory and add the following line, replacing YOUR_API_KEY with your actual LingQ API key:

```yml
LINGQ_API_KEY=YOUR_API_KEY
```

## Usage

To import `n` videos from YouTube channels as a lesson into LingQ, run the following command:

```bash
python run.py -n 50 channel1 channel2 channel3
```

Replace <YOUTUBE_VIDEO_URL> with the URL of the YouTube video you want to import.

## Contributing

Contributions are welcome! If you have any suggestions, bug reports, or feature requests, please open an issue or submit a pull request.
