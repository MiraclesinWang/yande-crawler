This is a development version of `yande-crawler` project.

## Usage:
1. make sure that you have all require modules installed.
2. make sure that you can access https://yande.re in your terminal.
2. in main.py, set which tags and how many pages you want to download.
3. run `python main.py` and wait.
4. images downloaded will be found in . or the path you set(recommended)

### Example
```py
main(tags=['loli', 'naked'], download_directory=r'D:\file\Pictures\yande', score_threshold=60)
```
Obviously, this is not quite convenient currently. Afterwards, I will develop a GUI for it.

## Development log:
 - 2021/11/25
    * use API instead of parsing HTML
    * add tqdm to indicate download progress
 - 2021/12/29
    * add multi-processing to accelerate the downloading
    * automatically allocate filename by index, this can organize the files orderly
    * automatically judge how many pictures need to be downloaded, you can also fix the number on your own, but make sure not exceeding the max available number
    * add retrying mechanism, if some images' downloadings fail (quite normal since server and web or vpn are not stable), the code can retry them afterwards. 
 - 2021/12/30
    * add image filtering according to the score given by the website. (according to the website, score is computed by thumbs-ups - thumbs-downs. Some tags tend to have high scores while others' are quite low, it is advised to try different scores for a tag to find the one you want)
    * fix some tiny bugs
    * to avoid dead cycle, add retrying times limit.
   
