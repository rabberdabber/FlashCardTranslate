# FlashCardTranslate

Welcome to FlashCardTranslate, A Flask Web Application that saves language flashcards with instant translation. The supported Languages are as follows: English, Spanish, French, German, Italian, Simplified Chinese, Japanese, Korean, Vietnamese, Traditional Chinese.

Each user can create different categories with source and target language and add flashcards to those categories.

## Used Languages/Frameworks/Databases/technologies
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![AWS](https://img.shields.io/badge/AWS-%23FF9900.svg?style=for-the-badge&logo=amazon-aws&logoColor=white)



## DEMO
![DemoGIF](./FlashCardTranslate.gif)

## Application Links

- [Link to FlashCardTranslate](https://rabberdabber.dpgon835n9iag.ap-northeast-2.cs.amazonlightsail.com/) 
- [DEMO VIDEO ON YOUTUBE](https://www.youtube.com/watch?v=5PazVSe5JI8&t=4s&ab_channel=bereketsiyum)

## Description
- FlashCardTranslate is a database-backed application so Create,Read,Update,Delete(CRUD) operations are applied to save,read,delete the flashcards. I used a PostgreSQL Database to Save the Categories and Flashcard contents. The Translation are made by using NAVER Papago Translation API.
- IAM(Identity Access Management) is used for authentication and authorization of users.Specifically I used AUTH0's API and authlib python library. 
- It is also a RESTful application as we can use endpoints to manipulate the flashcards or database but each user will be given specific JWT tokens for the REST API after login for authorization sake. 
- Test Driven Development(TDD) using python unittest is employed to test the REST API each time there is a change in the application. 
- I used HTML/CSS/Javascript and Bootstrap to make minimal UI.
- Finally, I used docker to containerize the Flask Application along with gunicorn server and deployed it on AWS.

![Screen Shot 2022-07-06 at 2 22 46 PM](https://user-images.githubusercontent.com/60803336/177474975-d9ea3ffe-d600-430b-bda8-82aa629504dc.png)


## REST API

This documentation aims to be a comprehensive aid in using the the REST API endpoints to get/add/delete cards in the categories. The API follows RESTful design principles & best practices.


**user** - using language categories and flashcards
`create:category`
`read:category`
`delete:category`
`create:card`
`delete:card`
`read:card`

---

## List of all endpoints

## Categories endpoints
[`GET /categories/json`](#get-categories)  
[`GET /categories/:id/json`](#get-categoriesid)  
[`POST /categories/json`](#post-categories)   
[`DELETE /categories/:id/json`](#delete-categoriesid)

## Cards endpoints
[`GET /categories/:id/cards/json`](#get-categoriesidcards)  
[`POST /cards/:id/json`](#post-cardsid)   
[`POST /cards/json`](#post-cards)   
[`DELETE /cards/:id/json`](#delete-cardsid) 

## Endpoints in detail
- To get all categories choose GET categories and leave others as they are. Below is a sample request.
![Screen Shot 2022-07-06 at 11 16 41 PM](https://user-images.githubusercontent.com/60803336/177572642-a62998f1-c032-44d4-bc66-9246d0ee5564.png)

- To post a category choose POST category and also input source and target languages. Below is a sample request.
![Screen Shot 2022-07-06 at 11 18 24 PM](https://user-images.githubusercontent.com/60803336/177572689-42e59e1c-aabb-4c36-a129-3d95ee0025da.png)

- After posting category, we can see that new category is created as below.
![Screen Shot 2022-07-06 at 11 19 06 PM](https://user-images.githubusercontent.com/60803336/177575232-f4346d5b-547a-4482-a6a2-24f0547c8d15.png)
 
- To post a card choose POST card and also input source and language target and word. Below is a sample request.
![Screen Shot 2022-07-06 at 11 18 48 PM](https://user-images.githubusercontent.com/60803336/177572702-0deb1360-d84d-4df4-ae56-9ef4a51381a4.png)

- After posting a flashcard, we can see that new flashcard with a word hello is created as below.
![Screen Shot 2022-07-06 at 11 19 18 PM](https://user-images.githubusercontent.com/60803336/177575514-68be82c2-dcf0-4623-ab58-8bf287345f18.png)

- To delete a category choose DELETE category and also input category ID. Below is a sample request.
![Screen Shot 2022-07-06 at 11 24 16 PM](https://user-images.githubusercontent.com/60803336/177575670-46163268-e9a7-4724-82b5-59124e668473.png)

- As we can see, the category is deleted.
![Screen Shot 2022-07-06 at 11 24 29 PM](https://user-images.githubusercontent.com/60803336/177575689-2a8bd63c-9f60-4d1c-87d3-394a6d4e6f3e.png)



*You can check the REST api in the API navigation bar after you login to the application. the REST api requires JWT tokens as the application employs IAM(Identification Access Management) to authenticate and authorize users*


## Authors

+ Bereket Assefa

