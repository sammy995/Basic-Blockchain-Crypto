**Command Reference**
Activate the virtual environment

```
.\blockchain-env\Scripts\activate
```

**Install all packages**

```
py install -r requirements.txt
```

**Run the tests**

Make sure to activate the virtual environment.

```
py -m pytest backend/tests
```

**Run the application and API**

Make sure to activate the virtual environment.

```
py -m backend.app
```

**Run a peer instance**

Make sure to activate the virtual environment.

```
export PEER=True && py -m backend.app
```

**Run the frontend**

In the frontend directory:

```
npm run start
```

**Seed the backend with data**

Make sure to activate the virtual environment.

```
export SEED_DATA=True && py -m backend.app
```
