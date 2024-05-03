# Summanry
I have created a class to store and use data saved in any app's Shared Preferences. This way you can save boolean, int, string data or check if data has been saved in a specific group of preferences for your app.

So, you need to create a class "StoredPreferences.java" and put the content down bellow. Also I'm going to leave some examples about how to use it.

I hope it can helps you

# Usage
## For an Activity
```
 //// To Save a value
 DataProccessor dataProccessor = new DataProccessor(this);
 dataProccessor.setStr("email","johndoe@mail.com");

 //// To Retreive a value
 dataProccessor.getStr("email")
 ```
## For a Fragment
```
//// To Save a value
 DataProccessor dataProccessor = new DataProccessor(getActivity());
 dataProccessor.setStr("email","johndoe@mail.com");

 //// To Retreive a value
 dataProccessor.getStr("email");
```
## For a Service
```
 //// To Save a value
 DataProccessor dataProccessor = new DataProccessor(getApplicationContext());
 dataProccessor.setStr("email","johndoe@mail.com");

 //// To Retreive a value
 dataProccessor.getStr("email");
```