const express = require('express');
const app = express();
const morgan = require('morgan');
const bodyparser = require('body-parser');
const mongoose = require('mongoose');

const cnnRoutes = require('./api/routes/cnn');

const svmRoutes = require('./api/routes/svm');

mongoose.connect('mongodb+srv://labelling:'+
    process.env.MONGO_ATLAS_PW+
    '@ecglabelling-zkauy.azure.mongodb.net/test?retryWrites=true',
    {
        useNewUrlParser: true
    });

app.use(morgan('dev'));
app.use(bodyparser.urlencoded({extended:false}));
app.use(bodyparser.json());
app.use('/uploads',express.static('uploads'))
app.use(( req, res, next)=>{
    res.header("Access-Control-Allow-Origin","*");
    res.header(
        "Access-Control-Allow-Headers",
        "Origin, X-Requested-With, Content-Type, Accept, Authorization"
    );
    if (req.method === 'OPTIONS'){
        res.header(
            'Access-Control-Allow-Methods',
            'PUT, POST, PATCH, DELETE, GET');
        return res.status(200).json({});
    }
    next();
});

//api routes
app.use('/cnn',cnnRoutes);
app.use('/svm',svmRoutes);

// 404 routes
app.use((req,res,next)=>{
    const error = new Error('Not found');
    error.status = 404;
    next(error);
})

app.use((error, req, res, next)=>{
    res.status(error.status|| 500);
    res.json({
        error :{
            message: error.message

        }
    })
})
module.exports = app ;