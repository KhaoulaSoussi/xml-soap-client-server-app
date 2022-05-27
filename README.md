# xml-soap-client-server-app

## Project Overview

This project is a minimal cloud drive application inspired from Google Drive. It allows the user to automatically back-up his/her files on the cloud. We would like to develop a language-agnostic solution for this problem using Java on server side and Python on the client side.

## Technology Enablers

1. Build Tool: Gradle  
Gradle (a Google open-source project) is a build tool that is extremely useful to handle all dependencies implementation on our behalf. It is supported by many IDEs including IntelliJ IDEA which is the IDE I used in this project.

2. Language-Agnostic Technology: XML/SOAP  
XML (Extensible Markup Language) is a metalanguage (general purpose language) that allows the designer of the XML file to create their own tags and define their own schema (e.g., tags hierarchy, types of attributes, values of tags...). XML leverages HTTP to handle web services, and it only uses one HTTP verb which is POST.  
For two different systems to communicate and exchange data in a language-independent way, they need to agree upon a contract which is the API. In an XML-based application, the language used to generate the API is XML. There are many XML-based interface definition languages, one of which is WSDL (Web Services Definition Language) which is the language used for XML/SOAP. SOAP (Simple Object Access Protocol) is the protocol that dictates the body part of the POST request.

3. Java Support for XML/SOAP: JAXWS   
JAXWS is the Java API for XML/SOAP. It provides tools useful for developing web services such as wsgen which is used to generate all the artifacts required for the web service. Wsgen generates the WSDL file, the client stub, and the server skeleton in Java. JAXWS also provides the Endpoint java class which provides the static method publish which is used to publish the business logic annotated with the @webservice annotation under a specified URL. The WSDL file describes the interface and also specifies the location of the service provider which is the URL.

4. Python SOAP Client: Zeep   
Zeep is a Python API for XML/SOAP. It inspects the WSDL file containing the service
provider URL and interface, and it generates the corresponding stub to use the services provided by the SOAP server.

## Implementation Details

The technology I used to support language-independence is XML/SOAP. I followed a code-first approach to implement the proposed solution. Here is a detailed description of the steps performed during the development process:

1. Develop the Java service provider  
Under cloud.provider package, the provider-side code resides. The Backup class which contains the business logic is annotated with the JAXWS `@webservice` annotation to tell the Java Runtime Environment to expose all the public methods in the class as XML/SOAP web services. Three public methods are defined in this class: the method `create_backup_folder` takes a folder name and creates it under the project root directory; the method `upload_file` takes the file name, the file size, and the file array of bytes and creates the corresponding file under the cloud backup folder; finally, the method `delete_file` takes the file name and deletes it from the backup folder.  
Under the same package is the Provider main class which instantiates the cloud drive business implementation and publishes it as a web service under the URL http://localhost:9000/backup using the publish static method of the Endpoint class provided by JAXWS.

2. Generate the WSDL file and the Java server skeleton  
After building the Java service provider using Gradle build command: ./gradlew build, I generated the WSDL file using the command line tool wsgen by running the following command:
`wsgen -wsdl -cp build/classes/java/main/ -d build/classes/java/main/ - r src/main/resources/ cloud.provider.Backup`. In the generated WSDL file, I changed the value of soap:address location tag to http://localhost:9000/backup.

3. Develop the Python service consumer    
The Python service consumer uses the Python module Zeep which takes the path to the wsdl file and generates the corresponding client stub.  
The client code starts by issuing a `create backup folder` request to the server by calling the method `create_backup_folder`. The client then sends all the local files to be stored in the cloud folder by repeatedly calling the upload method.  
As long as the connection is held between the server and the client, this latter keeps checking for any changes that might occur to the files contained in the local folder. If any file was added or modified, it is automatically sent to the server using the upload method; if any file was deleted, the user is asked to confirm or deny the deletion from the backup folder.

4. Run the Java provider    
The Java provider can be ran using the Gradle command `./gradlew run`.

5. Run the Python service consumer   
Before running the Python code, the folder to be backed up in the cloud should be placed under the same directory as the Python code. Then the Python code can be ran using the command:  
`python3 src/main/python/consumer.py path_to_local_folder`

