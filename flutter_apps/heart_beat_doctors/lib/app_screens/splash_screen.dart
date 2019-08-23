import 'package:flutter/material.dart';
import 'dart:math';
import 'dart:async';
import 'package:heart_beat_doctors/app_screens/home_screen.dart';

class SplashScreen extends StatefulWidget {
  @override
  _SplashScreenState createState() => _SplashScreenState();
}

class _SplashScreenState extends State<SplashScreen>
    with SingleTickerProviderStateMixin {
  AnimationController _controller;
  double square_width = 15.0;

  @override
  void initState() {
    // TODO: implement initState
    super.initState();
    loadSplash();
    _controller =
        AnimationController(vsync: this, duration: Duration(milliseconds: 1500));
    _controller.repeat();

  }

  Future<Timer> loadSplash() async{

    return new Timer(Duration(milliseconds: 3000),onDoneLoading);
  }

  onDoneLoading() async{
    Navigator.of(context).pushReplacement(MaterialPageRoute(builder: (context) => HomeScreen()));
  }

  buildSquare(double delay) {
    return Row(
      children: <Widget>[
        FadeTransition(
            opacity: new TestTween(begin: 0.4, end: 1.0, delay: delay)
                .animate(_controller),
            child: Square(
              width: square_width,
              color: Colors.white,
            )),
        Padding(
          padding: EdgeInsets.only(right: 10.0),
        ),
      ],
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Stack(
        fit: StackFit.expand,
        children: <Widget>[
          Container(
            color: Colors.blue,
          ),
          Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: <Widget>[
              Text(
                'HeartBeat',
                style: TextStyle(
                    decoration: TextDecoration.none,
                    fontSize: 45.0,
                    fontFamily: 'Raleway',
                    fontWeight: FontWeight.w700,
                    color: Colors.white),
              ),
              Padding(
                padding: EdgeInsets.only(top: 40.0),
              ),
              Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: <Widget>[
                  buildSquare(.0),
                  buildSquare(.2),
                  buildSquare(.4),
                  buildSquare(.6),
                ],
              ),
            ],
          )
        ],
      ),
    );
  }

  @override
  void dispose() {
    // TODO: implement dispose
    _controller.dispose();
    super.dispose();
  }
}

class Square extends StatelessWidget {
  final double width;
  final Color color;

  Square({this.width, this.color});

  @override
  Widget build(BuildContext context) {
    return Container(
      width: this.width,
      height: this.width,
      decoration: BoxDecoration(color: this.color, shape: BoxShape.rectangle),
    );
  }
}

class TestTween extends Tween<double> {
  final double delay;

  TestTween({double begin, double end, this.delay})
      : super(begin: begin, end: end);

  @override
  double lerp(double t) {
    return super.lerp((sin((t - delay) * 2 * pi) + 1) / 2);
  }
}
