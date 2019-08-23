import 'package:flutter/material.dart';
import 'home_screen.dart';





class FinalResult extends StatefulWidget {
  final Map<String, int>  diseases;  //{"N":30,"S":100,"L":0,"B":60,"R":30};



  FinalResult({this.diseases});


  @override
  _FinalResultState createState() => _FinalResultState();
}

class _FinalResultState extends State<FinalResult> {
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
                margin: EdgeInsets.all(20.0),
                child: Column(
                  mainAxisSize: MainAxisSize.min,
                  children: <Widget>[
                    Padding(
                      padding: EdgeInsets.only(top: 20.0),
                    ),
                    Text(
                      'Results of your ECG analysis',
                      style: TextStyle(
                        decoration: TextDecoration.none,
                        fontFamily: 'Raleway',
                        fontSize: 22.0,
                      ),
                    ),
                    Padding(
                      padding: EdgeInsets.only(top: 20.0),
                    ),
                    Text(
                      'N: normal, S: sweet, L: Large',
                      style: TextStyle(
                        decoration: TextDecoration.none,
                        fontFamily: 'Raleway',
                        fontSize: 13.0,
                      ),
                    ),
                    Padding(
                      padding: EdgeInsets.only(top: 5.0),
                    ),
                    Text(
                      'B: black, R: rubby',
                      style: TextStyle(
                        decoration: TextDecoration.none,
                        fontFamily: 'Raleway',
                        fontSize: 13.0,
                      ),
                    ),
                    Padding(
                      padding: EdgeInsets.only(top: 30.0),
                    ),
                    MyProgressBar(
                      type: 'N',
                      value: widget.diseases["N"],
                    ),
                    MyProgressBar(
                      type: 'S',
                      value: widget.diseases["S"],
                    ),
                    MyProgressBar(
                      type: 'L',
                      value: widget.diseases["L"],
                    ),
                    MyProgressBar(
                      type: 'B',
                      value: widget.diseases["B"],
                    ),
                    MyProgressBar(
                      type: 'R',
                      value: widget.diseases["R"],
                    ),
                    Padding(
                      padding: EdgeInsets.only(top: 50),
                    ),
                    ButtonTheme.bar(
                      // make buttons use the appropriate styles for cards
                      child: ButtonBar(
                        children: <Widget>[
                          FlatButton(
                            child: const Text('RETRY'),
                            onPressed: () {
                              Navigator.of(context).push(MaterialPageRoute(
                                  builder: (context) => HomeScreen()));
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

class MyProgressBar extends StatefulWidget {
  final int value;
  final String type;

  MyProgressBar({this.value, this.type});

  @override
  _MyProgressBarState createState() => _MyProgressBarState();
}

class _MyProgressBarState extends State<MyProgressBar> {
  @override
  Widget build(BuildContext context) {
    return Container(
      padding: EdgeInsets.all(10.0),
      child: Row(
        children: <Widget>[
          Container(
            width: 50,
            padding: EdgeInsets.all(5),
            child: Text(
              '${widget.type}',
              textAlign: TextAlign.center,
              style: TextStyle(
                decoration: TextDecoration.none,
                fontFamily: 'Raleway',
                fontSize: 15.0,
              ),
            ),
          ),
          Expanded(
            child: Container(
              margin: EdgeInsets.all(5),
              padding: EdgeInsets.all(10.0),
              child: LinearProgressIndicator(
                value: widget.value * .01,
              ),
            ),
          ),
          Container(
            width: 50,
            padding: EdgeInsets.all(5),
            child: Text(
              '${widget.value}%',
              style: TextStyle(
                decoration: TextDecoration.none,
                fontFamily: 'Raleway',
                fontSize: 15.0,
              ),
            ),
          ),
        ],
      ),
    );
  }
}
