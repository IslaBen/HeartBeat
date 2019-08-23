import 'package:flutter/material.dart';
import 'upload_file_screen.dart';
import 'upload_image_screen.dart';

class HomeScreen extends StatelessWidget {
  Widget showHome(context) {
    return OrientationBuilder(builder: (context, orientation) {
      if (orientation == Orientation.portrait)
        return Portrait();
      else
        return Landscape();
    });
  }

  Widget Portrait() {
    return Center(
        child: Column(
      children: <Widget>[
        Padding(
          padding: EdgeInsets.only(top: 50.0),
        ),
        Expanded(
          child: MyCard(
            text: 'Upload a picture of your ECG',
            image: 'images/ecg.png',
            picture: true,
            file: false,
          ),
        ),
        Padding(
          padding: EdgeInsets.only(top: 20.0),
        ),
        Expanded(
          child: MyCard(
            text: 'Upload an ECG file',
            image: 'images/file.png',
            file: true,
            picture: false,
          ),
        ),
        Padding(
          padding: EdgeInsets.only(top: 50.0),
        ),
      ],
    ));
  }

  Widget Landscape() {
    return Center(
        child: Column(
      mainAxisAlignment: MainAxisAlignment.center,
      children: <Widget>[
        Row(
          children: <Widget>[
            Padding(
              padding: EdgeInsets.all(30.0),
            ),
            Expanded(
              child: MyCard(
                text: 'Upload a picture of your ECG',
                image: 'images/ecg.png',
                picture: true,
                file: false,
              ),
            ),
            Padding(
              padding: EdgeInsets.all(10.0),
            ),
            Expanded(
              child: MyCard(
                text: 'Upload an ECG file',
                image: 'images/file.png',
                file: true,
                picture: false,
              ),
            ),
            Padding(
              padding: EdgeInsets.all(30.0),
            ),
          ],
        )
      ],
    ));
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'HeartBeat',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: Scaffold(
        appBar: AppBar(
          title: Text("HeartBeat"),
        ),
        body: showHome(context),
      ),
    );
  }
}

class MyCard extends StatelessWidget {
  final String text;
  final String image;
  bool picture = false;
  bool file = false;

  MyCard({this.text, this.image, this.picture, this.file});

  nextPage(context) {
    if (picture){
      Navigator.of(context)
          .push(MaterialPageRoute(builder: (context) => UploadImage()));

    }
    else if (file)
      Navigator.of(context)
          .push(MaterialPageRoute(builder: (context) => UploadFile()));
  }

  @override
  Widget build(BuildContext context) {
    return RaisedButton(
      elevation: 4.0,
      color: Colors.white,
      onPressed: () {
        // do somthing
        nextPage(context);
      },
      child: Container(
        child: Column(
          children: <Widget>[
            Padding(
              padding: EdgeInsets.only(top: 20.0),
            ),
            Text(
              text,
              style: TextStyle(
                decoration: TextDecoration.none,
                fontFamily: 'Raleway',
                fontSize: 20.0,
              ),
            ),
            Padding(
              padding: EdgeInsets.only(top: 30.0),
            ),
            Image.asset(
              image,
              width: 300.0,
              height: 200.0,
            ),
          ],
        ),
        width: 320.0,
      ),
    );
  }
}
