Documentation of the command line interface of Instrumentum sanae Doctrinae 
===========================================================================


The CLI app have main commands and each commands have its specific subcommands. 
The avalaible command are : monergism, sermonindex, etc


# Documentation of the monergism command 


The **monergism** command allows the user to interact with [Monergism](https://www.monergism.com).
The **monergism** command has many subcommands. The subcommands are : 

- scrap_list
- scrap_general_information

## 1- scrap_list

### Presentation 
This command connect to [Monergism](https://www.monergism.com) and download the list of authors,
topics and bible books from this respective urls

- [https://www.monergism.com/authors](https://www.monergism.com/authors) for authors/speakers
- [https://www.monergism.com/topics](https://www.monergism.com/topics) for topics 
- [https://www.monergism.com/scripture](https://www.monergism.com/scripture) for bible books  

### Arguments

- output_folder
    This subcommand takes a required parameter **output_folder** which must be provided. It is a folder 
    where the data downloaded will be stored. 

Here is an example of code 

```console
$ "code_env/bin/python"  "cli_interface/argument_parser.py" monergism scrap_list output_folder="test_folder"
```


## 2- scrap_general_information

### Presentation 

This command scrap the general information about an author, topic or bible book. 
This general information is the html file of the page presenting the author and an a json 
file containing the information about the pages of the author. Here is the example of the 
speakers CH Spurgeon on the monergism 

### Arguments
This command takes tree arguments : 

- browse_by_type 

    It can be "topic", "speaker", "scripture". To precise if the target_name comming after 
    is a topic, a speaker or a bible book. 

- target_name 

    The name of the targeted topic, speaker or bible books. If "C H Spurgeon", it is
    the general information of Spurgeon which will be downloaded. To download for all topics, speakers
    or scriptures, put "all"

- output_folder 

    It the the output folder where the download data will be placed. 
    Here is an example to download the general information of all the topics. 


### Examples 

```console
$ "code_env/bin/python" "cli_interface/argument_parser.py" monergism scrap_general_information topic all "test_folder"
```

Here is an example to download the general information of all the speakers. 

```console 
$ "code_env/bin/python" "cli_interface/argument_parser.py" monergism scrap_general_information speaker all "test_folder"
``` 

Here is an example to download the general information of all the bible books. 

```console
$ "code_env/bin/python cli_interface/argument_parser.py monergism scrap_general_information scriptures all "test_folder"
``` 

Here is an example to download the general information of Spurgeon. 

```console
$ "code_env/bin/python cli_interface/argument_parser.py monergism scrap_general_information speaker "C H Spurgeon" "test_folder"
```

The same syntax used for Spurgeon can be used for any topic, speaker or bible books




## 3- scrap_work 

### Presentation 

This command download the works a topic, a speaker or a bible book. 
Works here are the not the file(pdf, html, etc). It is the content the pages presenting 
all the works of an author, topic or bible books. The script to download the works is 
recursive. There is a non zero probability that it may stuck in a infinite loop though it never 
happenned during my tests. 

This command takes tree arguments.

### Arguments 

- browse_by_type 
    It can be "topic", "speaker", "scripture". To precise if the target_name comming after 
    is a topic, a speaker or a bible book. 


- target_name 
    The name of the targeted topic, speaker or bible books. If "C H Spurgeon", it is
    the works of Spurgeon which will be downloaded. To download for all topics, speakers
    or scriptures, put "all"

- output_folder 
    It the the output folder where the download data will be placed. 

### Examples 

Here is an example to download the general information of all the topics. 

```console
$ "code_env/bin/python" "cli_interface/argument_parser.py" monergism scrap_work topic all "test_folder"
``` 


Here is an example to download the general information of all the speakers. 

```console    
$ "code_env/bin/python" "cli_interface/argument_parser.py" monergism scrap_work speaker all "test_folder"
```

Here is an example to download the general information of all the bible books. 

```console    
$ "code_env/bin/python" "cli_interface/argument_parser.py" monergism scrap_work scriptures all "test_folder"
```

Here is an example to download the general information of Spurgeon. 

```console
$ "code_env/bin/python" "cli_interface/argument_parser.py" monergism scrap_work speaker "C H Spurgeon" "test_folder"
``` 

The same syntax used for Spurgeon can be used for any topic, speaker or bible books


# Documentation of the sermonindex command 

The **sermonindex** command allows the user to interact with (https://www.sermonindex.net/)[https://www.sermonindex.net/].

The **sermonindex** command has many subcommands. The subcommands are : 

- scrap_list
- scrap_general_information

## 1- scrap_list

### Presentation 

This command conntect to sermonindex and download the list of authors, books, etc 

- For the audio files 

    - It connect and download the list of authors from [https://www.sermonindex.net/modules/mydownloads/](https://www.sermonindex.net/modules/mydownloads/) as well as the other pages presenting authors (links with a tilde ~ at their begining)

    - It connect and download the list of topics from [https://www.sermonindex.net/modules/mydownloads/scr_index.php?act=topicsList](https://www.sermonindex.net/modules/mydownloads/scr_index.php?act=topicsList) as well as the other pages presenting authors (links with a tilde ~ at their begining)

    - It connect and download the list of bible books from [https://www.sermonindex.net/modules/mydownloads/scr_index.php?act=booksList](https://www.sermonindex.net/modules/mydownloads/scr_index.php?act=booksList) 
 
    - It connect finaly and download the list of podcasts from [https://www.sermonindex.net/podcast.php]
    (https://www.sermonindex.net/podcast.php)



- For documents 
    - It connect and download the list of authors from [https://www.sermonindex.net/modules/articles/](https://www.sermonindex.net/modules/articles/) as well as the other pages presenting authors (links with a tilde ~ at their begining)

    - It connect and download the list of books from [https://www.sermonindex.net/modules/bible_books/?view=books_list](https://www.sermonindex.net/modules/bible_books/?view=books_list)


- For videos 
    - It connect and download the list of authors from [https://www.sermonindex.net/modules/myvideo/](https://www.sermonindex.net/modules/myvideo/) as well as the other pages presenting authors (links with a tilde ~ at their begining)

- For vintage images 
    - It connect and download the list of authors from [https://www.sermonindex.net/modules/myalbum/index.php](https://www.sermonindex.net/modules/myalbum/index.php) as well as the other pages presenting authors (links with a tilde ~ at their begining)


### Arguments 

- output_folder 
    This parameters is outputfolder where the scraped data will be saved as the html files 

### Examples 

```console
$ "bin/python" "argument_parser.py" sermonindex scrap_list output_folder="/home/elvis/Documents/ForGod/Scraping General/test_folder"
```

## 2 - scrap_general_information

### Description 

This command download the general information of the works of a author, topic, etc. 
This method download general information of 
- For the audio format 
    - speakers
    - topics
    - podcasts

- For the text format 
    - speakers 
    - christian books 

- For the video format 
    - speakers 

- For the vintage images 
    - speakers 


### Arguments 

- browse_by_type
    - For audio format: 
        The possible values are :  **speaker**, **topic**, **scripture** 
    - For text format
        The possible values are : **speaker** or **christian_book**
    - For video format
        The possible values are : **speaker** 
    - For vinttage image: 
        The possible values are : **speaker** 

- material_type  
    It is the parameter that sets if we are working with audio, text, video or vintage image. 
    The possible values are : **audio**,**text**,**video**,**vintage_image**

- target
    The targeted element. It can be a particular author, topic, book, etc. 
    To target all the authors, topics, books use the value **all**. 

    
    To target a particular author for audio file, the name of the author must be given and the <browse_by_type> must be **speaker** and <material_type> be **audio** 
    
- output_folder 
    This parameter set the folder where the data have to be downloaded. 


### Examples 

#### Audio examples 

##### Speakers
- Download the general informations of all speakers for audio format 

```console 
$ "bin/python" "cli_interface/argument_parser.py" sermonindex scrap_general_information speaker audio all  "test_folder"
```

- Download the general informations of the speaker **Leonard Ravenhill** for audio format 

```console 
$ "bin/python" "cli_interface/argument_parser.py" sermonindex scrap_general_information speaker audio "Leonard Ravenhill" "test_folder"
```

##### Topics 

- Download the general informations of all topics for audio format 

```console 
$ "bin/python" "cli_interface/argument_parser.py" sermonindex scrap_general_information topic audio all  "test_folder"
```

- Download the general informations of the topic **Early Church** for audio format 

```console 
$ "bin/python" "cli_interface/argument_parser.py" sermonindex scrap_general_information topic audio "Early Church" "test_folder"
```

##### Scriptures

- Download the general informations of all scriptures for audio format 

```console 
$ "bin/python" "cli_interface/argument_parser.py" sermonindex scrap_general_information scripture audio all  "test_folder"
```

- Download the general informations of the bible book **Genesis** for audio format 

```console 
$ "bin/python" "cli_interface/argument_parser.py" sermonindex scrap_general_information scripture audio Genesis "test_folder"
```

#### Text examples 

##### Speakers 

- Download the general informations of all the speakers for text format  

```console 
$ "bin/python" "cli_interface/argument_parser.py" sermonindex scrap_general_information speaker text all  "test_folder"
```

- Download the general informations of the speaker **C.H. Spurgeon** for text format 

```console 
$ "bin/python" "cli_interface/argument_parser.py" sermonindex scrap_general_information speaker text "C.H. Spurgeon" "test_folder"
```

##### Christian books 

- Download the general informations of all the christian books for text format  

```console 
$ "bin/python" "cli_interface/argument_parser.py" sermonindex scrap_general_information christian_book text all "test_folder"
```

- Download the general informations of the book **Tertullian - On The Flesh Of Christ** for text format  

```console 
$ "bin/python" "cli_interface/argument_parser.py" sermonindex scrap_general_information christian_book text "Tertullian - On The Flesh Of Christ" "test_folder"
```

#### Video books
##### Speakers 

- Download the general information all the speakers for video 
```console 
$ "bin/python" "cli_interface/argument_parser.py" sermonindex scrap_general_information speaker video all "test_folder"
```

- Download the general informations of the speaker **Art Katz** for text video  

```console 
$ "bin/python" "cli_interface/argument_parser.py" sermonindex scrap_general_information speaker video "Art Katz" "test_folder"
```


#### Vintage images
##### Speakers 

- Download the general information all the speakers for vintage image 
```console 
$ "bin/python" "cli_interface/argument_parser.py" sermonindex scrap_general_information speaker vintage_image all "test_folder"
```

- Download the general informations of the speaker **C.H. Spurgeon** for vintage image  

```console 
$ "bin/python" "cli_interface/argument_parser.py" sermonindex scrap_general_information speaker vintage_image "C.H. Spurgeon" "test_folder"
```


## 3 - scrap_work 

### Description 

This command scrap the work of an authors, topic, bible book etc. 

This method scrap general information of 
- For the audio format 
    - speakers
    - topics
    - scriptures

- For the text format 
    - speakers 
    - christian books 

- For the video format 
    - speakers 

- For the vintage images 
    - speakers 



### Arguments 

- browse_by_type
    - For audio format: 
        The possible values are :  **speaker**, **topic**, **scripture** 
    - For text format
        The possible values are : **speaker** or **christian_book**
    - For video format
        The possible values are : **speaker** 
    - For vinttage image: 
        The possible values are : **speaker** 

- material_type  
    It is the parameter that sets if we are working with audio, text, video or vintage image. 
    The possible values are : **audio**,**text**,**video**,**vintage_image**

- target
    The targeted element. It can be a particular author, topic, book, etc. 
    To target all the authors, topics, books use the value **all**. 

    
    To target a particular author for audio file, the name of the author must be given and the <browse_by_type> must be **speaker** and <material_type> be **audio** 
    
- output_folder 
    This parameter set the folder where the data have to be downloaded. 


### Examples 

#### Audio examples 

##### Speakers
- Scrap the work of all speakers for audio format 

```console 
$ "bin/python" "cli_interface/argument_parser.py" sermonindex scrap_work speaker audio all "test_folder"
```

- Scrap the work of the speaker **Leonard Ravenhill** for audio format 

```console 
$ "bin/python" "cli_interface/argument_parser.py" sermonindex scrap_work speaker audio "Leonard Ravenhill" "test_folder"
```

##### Topics 

- Scrap the work of all topics for audio format 

```console 
$ "bin/python" "cli_interface/argument_parser.py" sermonindex scrap_work topic audio all  "test_folder"
```

- Scrap the work of the topic **Early Church** for audio format 

```console 
$ "bin/python" "cli_interface/argument_parser.py" sermonindex scrap_work topic audio "Early Church" "test_folder"
```

##### Scriptures

- Scrap the works of all scriptures for audio format 

```console 
$ "bin/python" "cli_interface/argument_parser.py" sermonindex scrap_work scripture audio all  "test_folder"
```

- Scrap the works of the bible book **Genesis** for audio format 

```console 
$ "bin/python" "cli_interface/argument_parser.py" sermonindex scrap_work scripture audio Genesis "test_folder"
```

#### Text examples 

##### Speakers 

- Scrap the works of all the speakers for text format  

```console 
$ "bin/python" "cli_interface/argument_parser.py" sermonindex scrap_work speaker text all  "test_folder"
```

- Scrap the works of the speaker **C.H. Spurgeon** for text format 

```console 
$ "bin/python" "cli_interface/argument_parser.py" sermonindex scrap_work speaker text "C.H. Spurgeon" "test_folder"
```

##### Christian books 

- Scrap the works of all the christian books for text format  

```console 
$ "bin/python" "cli_interface/argument_parser.py" sermonindex scrap_work christian_book text all "test_folder"
```

- Scrap the works of the book **Tertullian - On The Flesh Of Christ** for text format  

```console 
$ "bin/python" "cli_interface/argument_parser.py" sermonindex scrap_work christian_book text "Tertullian - On The Flesh Of Christ" "test_folder"
```

#### Video books
##### Speakers 

- Scrap the work all the speakers for video 
```console 
$ "bin/python" "cli_interface/argument_parser.py" sermonindex scrap_work speaker video all "test_folder"
```

- Scrap the work of the speaker **Art Katz** for text video  

```console 
$ "bin/python" "cli_interface/argument_parser.py" sermonindex scrap_work speaker video "Art Katz" "test_folder"
```


#### Vintage images
##### Speakers 

- Scrap the works all the speakers for vintage image 
```console 
$ "bin/python" "cli_interface/argument_parser.py" sermonindex scrap_work speaker vintage_image all "test_folder"
```

- Scrap the works of the speaker **C.H. Spurgeon** for vintage image  

```console 
$ "bin/python" "cli_interface/argument_parser.py" sermonindex scrap_work speaker vintage_image "C.H. Spurgeon" "test_folder"
```




## 4 - download 

### Description 

This command download the work of an authors, topic, bible book etc. 

This method download filees of 
- For the audio format 
    - speakers
    - topics
    - scriptures

- For the text format 
    - speakers 
    - christian books 

- For the video format 
    - speakers 

- For the vintage images 
    - speakers 



### Arguments 

- browse_by_type
    - For audio format: 
        The possible values are :  **speaker**, **topic**, **scripture** 
    - For text format
        The possible values are : **speaker** or **christian_book**
    - For video format
        The possible values are : **speaker** 
    - For vinttage image: 
        The possible values are : **speaker** 

- material_type  
    It is the parameter that sets if we are working with audio, text, video or vintage image. 
    The possible values are : **audio**,**text**,**video**,**vintage_image**

- target
    The targeted element. It can be a particular author, topic, book, etc. 
    To target all the authors, topics, books use the value **all**. 

    
    To target a particular author for audio file, the name of the author must be given and the <browse_by_type> must be **speaker** and <material_type> be **audio** 
    
- output_folder 
    This parameter set the folder where the data have to be downloaded. 


### Examples 

#### Audio examples 

##### Speakers
- Download the work of all speakers for audio format 

```console 
$ "bin/python" "cli_interface/argument_parser.py" sermonindex scrap_work speaker audio all "test_folder"
```

- Download the work of the speaker **Leonard Ravenhill** for audio format 

```console 
$ "bin/python" "cli_interface/argument_parser.py" sermonindex scrap_work speaker audio "Leonard Ravenhill" "test_folder"
```

##### Topics 

- Download the work of all topics for audio format 

```console 
$ "bin/python" "cli_interface/argument_parser.py" sermonindex scrap_work topic audio all  "test_folder"
```

- Download the work of the topic **Early Church** for audio format 

```console 
$ "bin/python" "cli_interface/argument_parser.py" sermonindex scrap_work topic audio "Early Church" "test_folder"
```

##### Scriptures

- Download the works of all scriptures for audio format 

```console 
$ "bin/python" "cli_interface/argument_parser.py" sermonindex scrap_work scripture audio all  "test_folder"
```

- Download the works of the bible book **Genesis** for audio format 

```console 
$ "bin/python" "cli_interface/argument_parser.py" sermonindex scrap_work scripture audio Genesis "test_folder"
```

#### Text examples 

##### Speakers 

- Download the works of all the speakers for text format  

```console 
$ "bin/python" "cli_interface/argument_parser.py" sermonindex scrap_work speaker text all  "test_folder"
```

- Download the works of the speaker **C.H. Spurgeon** for text format 

```console 
$ "bin/python" "cli_interface/argument_parser.py" sermonindex scrap_work speaker text "C.H. Spurgeon" "test_folder"
```

##### Christian books 

- Download the works of all the christian books for text format  

```console 
$ "bin/python" "cli_interface/argument_parser.py" sermonindex scrap_work christian_book text all "test_folder"
```

- Download the works of the book **Tertullian - On The Flesh Of Christ** for text format  

```console 
$ "bin/python" "cli_interface/argument_parser.py" sermonindex scrap_work christian_book text "Tertullian - On The Flesh Of Christ" "test_folder"
```

#### Video books
##### Speakers 

- Download the work all the speakers for video 
```console 
$ "bin/python" "cli_interface/argument_parser.py" sermonindex scrap_work speaker video all "test_folder"
```

- Download the work of the speaker **Art Katz** for text video  

```console 
$ "bin/python" "cli_interface/argument_parser.py" sermonindex scrap_work speaker video "Art Katz" "test_folder"
```


#### Vintage images
##### Speakers 

- Download the works all the speakers for vintage image 
```console 
$ "bin/python" "cli_interface/argument_parser.py" sermonindex scrap_work speaker vintage_image all "test_folder"
```

- Download the works of the speaker **C.H. Spurgeon** for vintage image  

```console 
$ "bin/python" "cli_interface/argument_parser.py" sermonindex scrap_work speaker vintage_image "C.H. Spurgeon" "test_folder"
```
