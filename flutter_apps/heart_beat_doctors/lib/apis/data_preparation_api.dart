import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:async';
import 'dart:convert';
import 'package:heart_beat_doctors/app_screens/result_screen.dart';

class DataPreparationAPI{

  static Widget upload(context){
    return Center(
      child: FutureBuilder(
        future: getUser(),
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return waiting();
          } else if (snapshot.hasData) {
            return result(context);
          } else if (snapshot.hasError) {
            return Row(
              children: <Widget>[
                Icon(Icons.refresh),
                Text('No internet connection'),
              ],
            );
          }
          return waiting();
        },
      ),
    );
  }

}



Widget result(context){
 return  ButtonTheme.bar(
   child: ButtonBar(
     children: <Widget>[
       FlatButton(
         child: const Text('RESULT'),
         onPressed: () {
           Navigator.of(context).push(MaterialPageRoute(
               builder: (context) =>  FinalResult(diseases: {"N":30,"S":100,"L":0,"B":60,"R":30},)));
         },
       ),
     ],
   ),
 );
}

Widget waiting(){
  return Column(
    mainAxisAlignment: MainAxisAlignment.center,
    children: <Widget>[
      Container(
          padding: EdgeInsets.only(top: 30, bottom: 30),
          child: Text(
            'Uploading',
            textAlign: TextAlign.center,
            style: TextStyle(
              decoration: TextDecoration.none,
              fontFamily: 'Raleway',
              fontSize: 18.0,
            ),
          )),
      Container(
        padding: EdgeInsets.only(left: 30,right: 30),
        child: LinearProgressIndicator(),
      ),

      Padding(
        padding: EdgeInsets.only(top: 30),
      ),

    ],
  );
}


Future<User> getUser() async {
  var url = 'https://reqres.in/api/users/2';
  var response = await http.get(url, headers: {'Accept': 'application/json'});
  if (response.statusCode == 200) {
    return User.fromJson(json.decode(response.body));
  } else {
    throw Exception('Failed to load post');
  }
}

class User {
  final int id;
  final String email;
  final String first_name;
  final String last_name;

  User({this.id, this.email, this.first_name, this.last_name});

  factory User.fromJson(Map<String, dynamic> json) {
    var data = json['data'];
    print('hello ${data['first_name']}');
    return User(
      id: data['id'],
      email: data['email'],
      first_name: data['first_name'],
      last_name: data['last_name'],
    );
  }
}
