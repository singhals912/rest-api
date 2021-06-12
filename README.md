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
5) Fetch a list of answered questions based on timestamp and models used

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

The requirements.txt file in current project installs -
* transformer - Transformers (formerly known as pytorch-transformers and pytorch-pretrained-bert) provides general-purpose architectures (BERT, GPT-2, RoBERTa, XLM, DistilBert, XLNet…) for Natural Language Understanding (NLU) and Natural Language Generation (NLG) with over 32+ pretrained models in 100+ languages and deep interoperability between Jax, PyTorch and TensorFlow. Importing these pretrained models which will allow our application to perform question answering task <br>
      
* PyTorch - PyTorch is based on Torch library used for applications such as computer vision and NLP. A number of HuggingFace's transformers are built on top of PyTorch. <br>
      
* Flask - Flask is a micro web framework written in Python. We use it to render UI and route various requests.

### Build and Run the API locally via Docker or Flask
A user can download this repository and after installing all the dependencies listed in requirement.txt, they can trigger the python code. Requests can be sent using application like 'Postman', instead of the application url, the user can hit their localhost and can continue to send the request following the routes specified above.

### Continuous Integration & Continuous Build (CI/CD)
Our application has been deployed to follow CI/CD principles and follows a consistent and automated way to build, package and deploy the application.<br>
We accomplish this by establishing workflow to Google Cloud using Actions in our GitHub. A workflow is a configurable automated process made up of one or more jobs. We have created a YAML file to define your workflow configuration. Once this workflow is established, any change in our repository sends an update request to our application deployed on google cloud. Below is how our workflow looks -<br>
<img src="/images/Build Deploy.PNG">
