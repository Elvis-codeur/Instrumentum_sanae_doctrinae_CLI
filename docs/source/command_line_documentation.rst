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



    This command takes two arguments.

    a) browse_by_type : It can be "topic", "speaker", "scripture". If it is "topic", it goes on and download 
    the general information of all the topics. The same for all the speakers or bible books if it is 
    respectively "speaker" or "topic". 

    It is also possible to send the name of particular topic, speaker or scripture. The app take the care to 
    find if the value given is a speaker, a topic or a scripture. However the parameter must be written as it is on 
    monergism. 

    Here is an example to download the general information of all the topics. 

.. code-block:: console
    
    $ "code_env/bin/python" "cli_interface/argument_parser.py" monergism scrap_general_information topic "test_folder"


Here is an example to download the general information of all the speakers. 

.. code-block:: console    
    
    $ "code_env/bin/python" "cli_interface/argument_parser.py" monergism scrap_general_information speaker "test_folder"


Here is an example to download the general information of all the bible books. 

.. code-block:: console    
    
    $ "code_env/bin/python cli_interface/argument_parser.py monergism scrap_general_information scriptures "test_folder


Here is an example to download the general information of Spurgeon. 

.. code-block:: console

    $ "code_env/bin/python cli_interface/argument_parser.py monergism scrap_general_information "C H Spurgeon" "test_folder

The same syntax used for Spurgeon can be used for any topic, speaker or bible books


    b) output_folder : It the the output folder where the download data will be placed. 



3- scrap_work 
    This command download the works a topic, a speaker or a bible book. 
    Works here are the not the file(pdf, html, etc). It is the content the pages presenting 
    all the works of an author, topic or bible books. The script to download the works is 
    recursive. There is a non zero probability that it may stuck in a infinite loop though it never 
    happenned during my tests. 
    

    This command takes two arguments.

    a) browse_by_type : It can be "topic", "speaker", "scripture". If it is "topic", it goes on and download 
    the works of all the topics. The same for all the speakers or bible books if it is 
    respectively "speaker" or "topic". 

    It is also possible to send the name of particular topic, speaker or scripture. The app take the care to 
    find if the value given is a speaker, a topic or a scripture. However the parameter must be written as it is on 
    monergism. 

    Here is an example to download the works of all the topics.

.. code-block:: console
    
    $ "code_env/bin/python" "cli_interface/argument_parser.py" monergism scrap_work topic "test_folder"


Here is an example to download the works of all the speakers. 

.. code-block:: console    
    
    $ "code_env/bin/python" "cli_interface/argument_parser.py" monergism scrap_work speaker "test_folder"


Here is an example to download the works of all the bible books. 

.. code-block:: console    
    
    $ "code_env/bin/python cli_interface/argument_parser.py monergism scrap_work scriptures "test_folder


Here is an example to download works of Spurgeon. 

.. code-block:: console

    $ "code_env/bin/python cli_interface/argument_parser.py monergism scrap_work "C H Spurgeon" "test_folder

The same syntax used for Spurgeon can be used for any topic, speaker or bible books


    b) output_folder : It the the output folder where the download data will be placed. 

