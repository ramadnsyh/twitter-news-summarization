# Twitter News Summarization

Twitter news summarization is a block of code that allows you to retweet certain tweet from twitter account and give replies to their posts with a summary of the article

![](./assets/example.png)


## Setup

Please download using zip or you can use `git clone` if you are familiar with `git` and go to inside the directory

```bash
git clone https://github.com/ramadnsyh/twitter-news-summarization.git
cd twitter-news-summarization
```

## Installation

- Install [miniconda](https://docs.conda.io/en/latest/miniconda.html#installing) first
- then create environment based on yml file
    ```
    $ conda env create -f environment.yml
    ```
- activate environment
    ```
    $ conda activate tweet_summarization
    ```
- optional: to deactivate environment
    ```
    $ conda deactivate
    ```

## Preparation

- Make [twitter developer app](https://developer.twitter.com/en/apps) first (If you have it already, you can skip this step)

- Get and regenerate

    - `API key`
    - `API secret key`
    - `Access token`
    - `Access token secret`

- Fill in `.env` template with

    ```env
    API_KEY=<Your api key>
    API_SECRET_KEY=<Your api secret key>
    ACCESS_TOKEN=<Your access token>
    ACCESS_SECRET_TOKEN=<Your access secret token>
    ```

## Usage

```bash
python tweet_summarization.py <twitter username> --count=5

# Example usage
python tweet_summarization.py cnbctech --count=5
```

###### **Option**:
  - `twitter username`: It should be twitter account for news such as `@cnbc`, `@cnbctech`, `@detikcom` and `@kompas`
  - `count`: total updated tweets you want to retweet