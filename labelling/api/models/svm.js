const mongoose = require('mongoose');

const svmSchema = mongoose.Schema({
    _id: mongoose.Schema.Types.ObjectId,
    file: {type: String,required: true},
    label: { type:Number,required:true},
});

module.exports = mongoose.model('Svm',svmSchema);