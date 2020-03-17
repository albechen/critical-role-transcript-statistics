## Critical Role Transcript Patterns
##### Datamined the transcripts for line distribution and sentiment analysis per cast member and episode

**Language:** Python (pandas, scipy, matplotlib, seaborn, TextBlob, os) </br>
**Other:** youtube-dl

Critical Role is a live action roleplaying show where voice actors gather to play Dungeon and Dragons. These sessions are streamed weekly on [Critical Role's Twitch Channel](https://www.twitch.tv/criticalrole) every Thursday since March 2015 and the team is currently on their second campaign of their series. Originally through fan support but now through professional means, the weekly live sessions are transcribed to be used as subtitles in their YouTube videos.

The goal of this study is to get a wholistic understanding of the cast’s line distribution, differences from campaign 1 and 2, and general sentimental patterns (using pre-generated sentiment analysis library from TextBlob). Using youtube-dl to scrape every episode's vtt subtitle file, the subtitles were cleaned and formatted in python to be analyzed.

The raw vtt files can be found in the data_raw folder and the processed datasets for the transcripts can be found in data_output. Finally, the process from vtt files to the analysis is summarized in the notebook:

[CR_transcript_analysis](https://github.com/albechen/critical-role-transcript-patterns/blob/master/CR_transcript_analysis.ipynb) which overviews:

1. Downloading subtitles from Critical Role playlist using youtube-dl
2. Open vtt formatted subtitles and process to readable format
3. Clean vtt to denote continuous lines and time stamps as dataframe
4. Create pipeline to process vtt for each episode in both campaigns
5. Aggregate data per cast member, episode, or campaign
6. Visualize data by pivoting through different aggregated formats

[CR_transcript_statistics](https://github.com/albechen/critical-role-transcript-patterns/blob/master/CR_transcript_statistics.ipynb) which overviews:

1. Automating ANOVA and Paired Z-test Functions
2. Preforming two-way ANOVA analysis across cast and season
3. Verify variation across cast and season with pairwise Z-test
4. Visualize all combinations of paired Z-test p-values

## Visualization
### Comparing Mean Talking Time (p-value Comparison)
![alt text](/images/pscore_all.png "pscore_all")

### Campaign 1
![alt text](/images/lineplot_per_ep_C1_nomatt.png "lineplot_per_ep_C1_nomatt")
![alt text](/images/density_time_per_ep_C1.png "density_time_per_ep_C1")
![alt text](/images/density_sentiment_C1.png "density_sentiment_C1")

### Campaign 2
![alt text](/images/lineplot_per_ep_C2_nomatt.png "lineplot_per_ep_C2_nomatt")
![alt text](/images/density_time_per_ep_C2.png "density_time_per_ep_C2")
![alt text](/images/density_sentiment_C2.png "density_sentiment_C2")
