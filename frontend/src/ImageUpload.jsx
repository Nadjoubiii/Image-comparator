import React, { useState } from 'react';
import axios from 'axios';
import './ImageUpload.css';

function ImageUpload() {
    const [file1, setFile1] = useState(null);
    const [file2, setFile2] = useState(null);
    const [file1Preview, setFile1Preview] = useState(null);
    const [file2Preview, setFile2Preview] = useState(null);
    const [result, setResult] = useState('');

    const handleFileChange = (e) => {
        const { name, files } = e.target;
        const file = files[0];
        if (file) {
            const filePreview = URL.createObjectURL(file);
            if (name === 'file1') {
                setFile1(file);
                setFile1Preview(filePreview);
            }
            if (name === 'file2') {
                setFile2(file);
                setFile2Preview(filePreview);
            }
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        const formData = new FormData();
        formData.append('file1', file1);
        formData.append('file2', file2);

        try {
            const response = await axios.post('http://127.0.0.1:5000/api/upload', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            });
            setResult(response.data.result);
        } catch (error) {
            console.error('There was an error uploading the files!', error);
        }
    };

    return (
        <div>
            <form onSubmit={handleSubmit}>
                <div className='wrapper'>
                    <label>Image 1:</label>
                    <input type="file" name="file1" onChange={handleFileChange} />
                    <img className="holder" width={250} height={160} src={file1Preview} alt="" />
                </div>
                <div className='wrapper'>
                    <label>Image 2:</label>
                    <input type="file" name="file2" onChange={handleFileChange} />
                    <img className="holder" src={file2Preview} width={250} height={160} alt="" />
                </div>
                <button type="submit">Upload and Compare</button>
                <img src="" alt="" />
            </form>
            {result && <div>Result: {result}</div>}
        </div>
    );
}

export default ImageUpload;
