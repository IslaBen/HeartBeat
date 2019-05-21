const express = require('express');
const router = express.Router();
const mongoose = require('mongoose');
const Cnn = require('../models/cnn');
const multer = require('multer');
const checkAuth = require('../middleware/check-auth');
const storage = multer.diskStorage({
    destination: function (req, file, cb) {
        cb(null,'./uploads/cnn/');
    },
    filename: function (req, file, cb) {
        cb(null,new Date().toISOString()+file.originalname);
    }
})

const upload = multer({storage:storage, limits: {
        fileSize: 1024*1024*3,
    }});

router.get('/',checkAuth,(req,res, next) => {
    Cnn.find()
        .select('file label _id')
        .exec()
        .then(docs=>{
            const response = {
                count: docs.length,
                product: docs.map(doc => {
                    return {
                        _id: doc._id,
                        file: doc.file,
                        label: doc.label,
                        request: {
                            type: 'GET',
                            url: process.env.domain+'cnn/'+doc._id
                        }
                    }
                })
            }
            res.status(200).json(response);
        })
        .catch(err=>{
            console.log(err);
            res.status(500).json({
                error:err
            });
        });
});

router.post('/',checkAuth, upload.single('entryFile'),(req,res, next) => {
    console.log(req.file);
    const cnn = new Cnn({
        _id : new mongoose.Types.ObjectId(),
        file : req.file.path,
        label: req.body.label
    });

    cnn.save()
        .then(result=>{
            console.log(result);
            res.status(200).json({
                entry:'CNN',
                createdEntry: {
                    _id: cnn._id,
                    file: cnn.file,
                    label: cnn.label,
                    request: {
                        type: 'GET',
                        url: process.env.domain+'cnn/' + cnn._id
                    }
                }
            });
        })
        .catch(err=>{
            console.log(err);
            res.status(500).json({
                error:err
            })
        });

});

router.get('/:cnnId',checkAuth,(req,res, next) => {
    const id = req.params.cnnId;
    Cnn.findById(id)
        .select('file label _id')
        .exec()
        .then(doc=>{
            console.log(doc);
            if (doc){
                const response = {
                    cnn:doc,
                    cnns:{
                        type:'GET',
                        description:"get all the cnn entries",
                        url:process.env.domain+'cnn/'
                    }
                }
                res.status(200).json(response);
            }else {
                res.status(404).json({
                    message:"no entry with that ID"
                });
            }
        })
        .catch(err=>{
            console.log(err);
            res.status(500).json({error:err});
        })
});

router.patch('/:cnnId',checkAuth,(req,res, next) => {
    const id = req.params.cnnId;
    const updateOpts = {};
    for (const ops of req.body){
        updateOpts[ops.propertyName] = ops.value;
    }
    Cnn.update({_id:id},{ $set:updateOpts})
        .exec()
        .then(result=>{
            res.status(200).json({
                message:"entry updated !!",
                request:{
                    type: 'GET',
                    description:"get details about the entry ",
                    url: process.env.domain+'cnn/'+id
                }
            });
        })
        .catch(err=>{
            console.log(err);
            res.status(500).json({
                error:err
            });
        });
});

router.delete('/:cnnId',checkAuth,(req,res, next) => {
    const id = req.params.cnnId;
    Cnn.remove({
        _id: id
    })
        .exec()
        .then(result=>{
            res.status(200).json({
                message:"entry deleted !!",
            });
        })
        .catch(err=>{
            console.log(err);
            res.status(500).json({
                error:err
            });
        });
});

module.exports = router;