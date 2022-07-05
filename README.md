# FlashCardTranslate

Welcome to FlashCardTranslate, A Flask Web Application that saves language flashcards with instant translation. The supported Languages are as follows: English, Spanish, French, German, Italian, Simplified Chinese, Japanese, Korean, Vietnamese, Traditional Chinese.

Each user can create different categories with source and target language and add flashcards to those categories.


## DEMO
![DemoGIF](./FlashCardTranslate.gif)

## Application URL
```
https://rabberdabber.dpgon835n9iag.ap-northeast-2.cs.amazonlightsail.com/
```

## DEMO


## REST API

This documentation aims to be a comprehensive aid in using the the REST API endpoints to get/add/delete cards in the categories. The API follows RESTful design principles & best practices.

---

**user** - using language categories and flashcards_  
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

*You can check the REST api in the API navigation bar after you login to the application. the REST api requires tokens as the application uses IAM(Identification Access Management)*


## Authors

+ Bereket Assefa

