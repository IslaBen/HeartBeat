const express = require('express');
const router = express.Router();
const mongoose = require('mongoose');
const Svm = require('../models/svm');
const multer = require('multer');
const checkAuth = require('../middleware/check-auth');

const storage = multer.diskStorage({
    destination: function (req, file, cb) {
        cb(null,'./uploads/svm/');
    },
    filename: function (req, file, cb) {
        cb(null,new Date().toISOString()+file.originalname);
    }
})

const upload = multer({storage:storage, limits: {
    fileSize: 1024*1024*3,
    }});

router.get('/',checkAuth,(req,res, next) => {
    Svm.find()
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
                            url: process.env.domain+'svm/'+doc._id
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

router.post('/',checkAuth,upload.single('entryFile'),(req,res, next) => {
    console.log(req.file);
    const svm = new Svm({
        _id : new mongoose.Types.ObjectId(),
        file : req.file.path,
        label: req.body.label
    });

    svm.save()
        .then(result=>{
            console.log(result);
            res.status(200).json({
                entry:'SVM',
                createdEntry: {
                    _id: svm._id,
                    file: svm.file,
                    label: svm.label,
                    request: {
                        type: 'GET',
                        url: process.env.domain+'svm/' + svm._id
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

router.get('/:svmId',checkAuth,(req,res, next) => {
    const id = req.params.svmId;
    Svm.findById(id)
        .select('file label _id')
        .exec()
        .then(doc=>{
            console.log(doc);
            if (doc){
                const response = {
                    svm:doc,
                    svms:{
                        type:'GET',
                        description:"get all the svm entries",
                        url:process.env.domain+'svm/'
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

router.patch('/:svmId',checkAuth,(req,res, next) => {
    const id = req.params.svmId;
    const updateOpts = {};
    for (const ops of req.body){
        updateOpts[ops.propertyName] = ops.value;
    }
    Svm.update({_id:id},{ $set:updateOpts})
        .exec()
        .then(result=>{
            res.status(200).json({
                message:"entry updated !!",
                request:{
                    type: 'GET',
                    description:"get details about the entry ",
                    url: process.env.domain+'svm/'+id
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

router.delete('/:svmId',checkAuth,(req,res, next) => {
    const id = req.params.svmId;
    Svm.remove({
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