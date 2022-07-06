# FlashCardTranslate

Welcome to FlashCardTranslate, A Flask Web Application that saves language flashcards with instant translation. The supported Languages are as follows: English, Spanish, French, German, Italian, Simplified Chinese, Japanese, Korean, Vietnamese, Traditional Chinese.

Each user can create different categories with source and target language and add flashcards to those categories.

[![PyPI - Python](https://img.shields.io/pypi/pyversions/iconsdk?logo=pypi)](https://pypi.org/project/iconsdk)

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
- I used HTML/CSS and Bootstrap to make minimal UI.
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

*You can check the REST api in the API navigation bar after you login to the application. the REST api requires JWT tokens as the application employs IAM(Identification Access Management) to authenticate and authorize users*


## Authors

+ Bereket Assefa

