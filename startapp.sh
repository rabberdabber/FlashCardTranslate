docker run --name flashcards -d -p 8000:8000 -e AUTH0_DOMAIN=dev-edb8aftf.us.auth0.com -e AUTH0_CLIENTID=8JOsdDgmRLEIBHyznccwV7g5j3fVgTnQ -e AUTH0_CLIENT_SECRET=X6upKpurHW638iZgScQysqtE-4-RuCBRTmZ3arLkaH_ISCJDf67iu14UgKWoZ4kb -e AUTH0_AUDIENCE=8JOsdDgmRLEIBHyznccwV7g5j3fVgTnQ -e SQLALCHEMY_DATABASE_URI=postgresql://dbmasteruser:b911ereket@ls-07d305c9ab59786a0fc5ea9b363343e142f12f1a.cojynopwd98o.ap-northeast-2.rds.amazonaws.com:5432/flashcard 20170844/flashcards:latest