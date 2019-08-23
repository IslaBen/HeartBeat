import 'package:flutter/material.dart';
import 'package:file_picker/file_picker.dart';
import 'home_screen.dart';
import 'result_screen.dart';

class UploadFile extends StatefulWidget {
  @override
  _UploadFileState createState() => _UploadFileState();
}

class _UploadFileState extends State<UploadFile> {
  String _path;
  String _fileName = '';
  String _extension = 'pat';
  bool confirm = false;

  confirmation(confirm) {
    setState(() {
      this.confirm = confirm;
    });
  }

  selectFile() async {
    var filePath = await FilePicker.getFilePath(
        type: FileType.CUSTOM, fileExtension: _extension);
    setState(() {
      _path = filePath;
      _fileName = _path != null ? _path.split('/').last : '...';
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
                  children: <Widget>[
                    _path == null
                        ? Container(
                            padding: EdgeInsets.only(top: 110),
                            width: 200,
                            height: 200,
                            child: Text(
                              'No file selected',
                              textAlign: TextAlign.center,
                              style: TextStyle(
                                decoration: TextDecoration.none,
                                fontFamily: 'Raleway',
                                fontSize: 15.0,
                              ),
                            ))
                        : Column(
                            children: <Widget>[
                              Container(
                                padding: EdgeInsets.only(top: 50, bottom: 50,right: 20,left:20 ),
                                child: Text(
                                  _fileName,
                                  textAlign: TextAlign.center,
                                  style: TextStyle(
                                    decoration: TextDecoration.none,
                                    fontFamily: 'Raleway',
                                    fontSize: 40.0,
                                  ),
                                ),
                              ),
                              Container(
                                child: Text(
                                  '',
                                  style: TextStyle(
                                    decoration: TextDecoration.none,
                                    fontFamily: 'Raleway',
                                    fontSize: 0.0,
                                  ),
                                ),
                              ),
                            ],
                          ),
                    confirm
                        ? Column(
                            mainAxisAlignment: MainAxisAlignment.center,
                            children: <Widget>[
                              Divider(),
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
                          )
                        : ButtonTheme.bar(
                            // make buttons use the appropriate styles for cards
                            child: ButtonBar(
                              children: <Widget>[
                                _path!= null
                                    ? FlatButton(
                                        child: const Text('CONFIRM'),
                                        onPressed: () {
                                          confirmation(true);
                                        },
                                      )
                                    : Container(),
                                FlatButton(
                                  child: const Text('SELECT'),
                                  onPressed: () {
                                    selectFile();
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
}
