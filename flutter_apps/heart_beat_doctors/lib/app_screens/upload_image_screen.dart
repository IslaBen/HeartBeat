import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import 'dart:async';
import 'dart:io';
import 'ajustment_screen.dart';
import 'package:heart_beat_doctors/apis/data_preparation_api.dart';


class UploadImage extends StatefulWidget {
  @override
  _UploadImageState createState() => _UploadImageState();
}

class _UploadImageState extends State<UploadImage> {
  File _image;
  bool confirm = false;

  confirmation(confirm) {
    setState(() {
      this.confirm = confirm;
    });
  }

  Future getImageFromCam() async {
    // for camera
    var image = await ImagePicker.pickImage(source: ImageSource.camera);
    setState(() {
      _image = image;
    });
  }

  Future getImageFromGallery() async {
    // for gallery
    var image = await ImagePicker.pickImage(source: ImageSource.gallery);
    setState(() {
      _image = image;
    });
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
          body: Center(
            child: SingleChildScrollView(
              child: Card(
                elevation: 4.0,
                margin: EdgeInsets.all(20),
                child: Column(
                  mainAxisSize: MainAxisSize.min,
                  children: <Widget>[
                    Container(
                      child: Center(
                        child: _image == null
                            ? Container(
                                padding: EdgeInsets.only(top: 110),
                                width: 200,
                                height: 200,
                                child: Text(
                                  'No image selected',
                                  textAlign: TextAlign.center,
                                  style: TextStyle(
                                    decoration: TextDecoration.none,
                                    fontFamily: 'Raleway',
                                    fontSize: 15.0,
                                  ),
                                ),
                              )
                            : Container(
                                child: Image.file(
                                _image,
                                fit: BoxFit.cover,
                              )),
                      ),
                    ),
                    confirm
                        ? DataPreparationAPI.upload(context)
                        : ButtonTheme.bar(
                            child: ButtonBar(
                              children: <Widget>[
                                _image != null
                                    ? FlatButton(
                                        child: const Text('CONFIRM'),
                                        onPressed: () {
                                          confirmation(true);
                                        },
                                      )
                                    : Container(),
                                _image != null
                                    ? FlatButton(
                                        child: const Text('AJUSTMENT'),
                                        onPressed: () {
                                          Navigator.of(context).push(
                                              MaterialPageRoute(
                                                  builder: (context) =>
                                                      AjustImage(
                                                        image: _image,
                                                      )));
                                        },
                                      )
                                    : Container(),
                                FlatButton(
                                  child: const Text('SELECT'),
                                  onPressed: () {
                                    selectImage();
                                  },
                                ),
                              ],
                            ),
                          ),
                  ],
                ),
              ),
            ),
          ),
        ));
  }

  void selectImage() {
    showModalBottomSheet(
        context: context,
        builder: (context) {
          return Container(
            height: 80,
            color: Color(0xFF737373),
            child: Container(
              child: _buildNavigationMenu(),
              decoration: BoxDecoration(
                color: Theme.of(context).canvasColor,
                borderRadius: BorderRadius.only(
                  topLeft: Radius.circular(10),
                  topRight: Radius.circular(10),
                ),
              ),
            ),
          );
        });
  }

  Row _buildNavigationMenu() {
    return Row(
      mainAxisAlignment: MainAxisAlignment.center,
      children: <Widget>[
        FlatButton(
          child: Icon(Icons.add_a_photo),
          onPressed: () {
            Navigator.pop(context);
            //..
            getImageFromCam();
          },
        ),
        Padding(
          padding: EdgeInsets.only(right: 100.0),
        ),
        FlatButton(
          child: Icon(Icons.wallpaper),
          onPressed: () {
            Navigator.pop(context);
            //..
            getImageFromGallery();
          },
        ),
      ],
    );
  }
}
