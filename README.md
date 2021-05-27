# Mgmt590-Assignment2 - Creating REST API and deploying the application on google cloud
### Submission Details
|Name|PUID|
|----|----|
|Esha Kaushal| 0032356932|

### Application Description
The application can be accessed using the URL - https://mgmt590-restapi-es7glm5rsq-uc.a.run.app

The application allows a user to perform the following operations user JSON based API requests -
1) Add a huggingface question answering model to the database
2) Fetch a list of all models currently present in the database
3) Delete a model of choice from the database 
4) Get a question answered by providing the question and context. User can even choose the model to answer the question
5) Fetch a list of answered questions based on timestamp and model used

### Expected Request Routes
1)  **Action 1 - Add a models** - This route allows a user to add a new model into the server and make it available for inference.<br>
      Method and path: **PUT /models** <br>
      Sample request paramaters & respones -<br>
    <img src="/images/Add a model.PNG">

2)  **Action 2 - List all available Models** - This route allows a user to obtain a list of the models currently loaded into the server and available for inference <br>
     Method and path: **GET /models** <br>
     Sample request paramaters & respones - <br>
    <img src="/images/Get a model.PNG">

3)  **Action 3 - Delete a models** - This route allows a user to delete an existing model on the server such that it is no longer available for inference. <br>
      Method and path: **DELETE /models?model=<model name>** <br>
      Sample request paramaters & respones - <br>
    <img src="/images/Delete a model.PNG">

4)  **Action 4 - Answer a Question** - This route uses one of the available models to answer a question, given the context provided in the JSON payload.<br>
     Method and path: **POST /answer?model=<model name>     <model name> is optional** <br>
     Sample request paramaters & respones - <br>
    <img src="/images/Answer.PNG">

5)   **Action 5 - List desired answered question** - This route allows a user to obtain a list of questions with answered based on timestamp and model <br>
     Method and path: **GET /answer?model=<model name>&start=<start timestamp>&end=<end timestamp>     <model name> is optional** <br>
     Sample request paramaters & respones -<br>
    <img src="/images/FetchAnswer.PNG">

### Dependencies
The application uses a lot of python packages and libraries. All the required packages are listed in the file **requirements.txt**. A user can simply executing the following command - <br>
```$ pip install -r requirements.txt``` and voila! all the program's dependencies will be downloaded, installed and ready to be used by the application.

### Build and Run the API locally via Docker or Flask
A user can download this repository and after installing all the dependencies listed in requirement.txt, they can trigger the python code. Requests can be sent using application like 'Postman', instead of the application url, the user can hit their localhost and can continue to send the request following the routes specified above.
