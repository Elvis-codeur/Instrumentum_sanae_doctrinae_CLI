Documentation of the command line interface of Instrumentum sanae Doctrinae 
===========================================================================


The CLI app have main commands and each commands have its specific subcommands. 
The avalaible command are : monergism, sermonindex, etc


Documentation of the monergism command 
--------------------------------------

The **monergism** command allows the user to interact with `Monergism <https://www.monergism.com>`_.
The **monergism** command has many subcommands. The subcommands are : 

    - scrap_list
    - scrap_general_information

1- scrap_list
    This command connect to `Monergism <https://www.monergism.com>`_ and download the list of authors,
    topics and bible books from this respective urls

    - https://www.monergism.com/authors for authors/speakers
    - https://www.monergism.com/topics for topics 
    - https://www.monergism.com/scripture for bible books  


    This subcommand takes a required parameter **output_folder** which must be provided. It is a folder 
    where the data downloaded will be stored. 

    Here is an example of code 

.. code-block:: console

    $ "code_env/bin/python"  "cli_interface/argument_parser.py" monergism scrap_list output_folder="test_folder"



2- scrap_general_information

    This command scrap the general information about an author, topic or bible book. 
    This general information is the html file of the page presenting the author and an a json 
    file containing the information about the pages of the author. Here is the example of the 
    speakers CH Spurgeon on the monergism 


    This command takes tree arguments.

    a) browse_by_type : It can be "topic", "speaker", "scripture". To precise if the target_name comming after 
    is a topic, a speaker or a bible book. 
    
    
    b) target_name : The name of the targeted topic, speaker or bible books. If "C H Spurgeon", it is
     the general information of Spurgeon which will be downloaded. To download for all topics, speakers
     or scriptures, put "all"


    Here is an example to download the general information of all the topics. 

.. code-block:: console
    
    $ "code_env/bin/python" "cli_interface/argument_parser.py" monergism scrap_general_information topic all "test_folder"


Here is an example to download the general information of all the speakers. 

.. code-block:: console    
    
    $ "code_env/bin/python" "cli_interface/argument_parser.py" monergism scrap_general_information speaker all "test_folder"


Here is an example to download the general information of all the bible books. 

.. code-block:: console    
    
    $ "code_env/bin/python cli_interface/argument_parser.py monergism scrap_general_information scriptures all "test_folder"


Here is an example to download the general information of Spurgeon. 

.. code-block:: console

    $ "code_env/bin/python cli_interface/argument_parser.py monergism scrap_general_information speaker "C H Spurgeon" "test_folder"

The same syntax used for Spurgeon can be used for any topic, speaker or bible books


    c) output_folder : It the the output folder where the download data will be placed. 



3- scrap_work 
    This command download the works a topic, a speaker or a bible book. 
    Works here are the not the file(pdf, html, etc). It is the content the pages presenting 
    all the works of an author, topic or bible books. The script to download the works is 
    recursive. There is a non zero probability that it may stuck in a infinite loop though it never 
    happenned during my tests. 

    This command takes tree arguments.

    a) browse_by_type : It can be "topic", "speaker", "scripture". To precise if the target_name comming after 
    is a topic, a speaker or a bible book. 
    
    
    b) target_name : The name of the targeted topic, speaker or bible books. If "C H Spurgeon", it is
     the works of Spurgeon which will be downloaded. To download for all topics, speakers
     or scriptures, put "all"


    Here is an example to download the general information of all the topics. 

.. code-block:: console
    
    $ "code_env/bin/python" "cli_interface/argument_parser.py" monergism scrap_work topic all "test_folder"


Here is an example to download the general information of all the speakers. 

.. code-block:: console    
    
    $ "code_env/bin/python" "cli_interface/argument_parser.py" monergism scrap_work speaker all "test_folder"


Here is an example to download the general information of all the bible books. 

.. code-block:: console    
    
    $ "code_env/bin/python cli_interface/argument_parser.py monergism scrap_work scriptures all "test_folder"


Here is an example to download the general information of Spurgeon. 

.. code-block:: console

    $ "code_env/bin/python cli_interface/argument_parser.py monergism scrap_work speaker "C H Spurgeon" "test_folder"

The same syntax used for Spurgeon can be used for any topic, speaker or bible books


    c) output_folder : It the the output folder where the download data will be placed. 

