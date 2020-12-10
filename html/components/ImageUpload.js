app.component('image-upload', {
    template:
    /*html*/
`
<div class="upload-dialog-item" id="form-wrapper">
    <form action="upload" enctype="multipart/form-data" @submit.prevent="onSubmit">
        <input id="single-file" type="file" name="files" multiple v-on:change="onChange"/><br />
        <label class="label-button" id="single-file-label" for="single-file">Add Files</label>
    </form>
</div>
<div class="upload-dialog-item" id="upload-file-list">
    <ul>
        <li v-for="file in files" :key="file.index">
            <div class="upload-file-list-item">
                <button v-on:click="removeFile(file.index)">X</button>
            </div>
            <div class="upload-file-list-item">
                {{ file.file.name }} - 
            </div>
            <div class="upload-file-list-item">
                {{ file.state }}
            </div>
        </li>
    </ul>
</div>
<div class="upload-dialog-item">
    <div>
        <button :disabled="files.length == 0 || uploading > 0" v-on:click="uploadFiles">Upload Files</button>
    </div>
</div>
`,
    data() {
        return {
            files: [],
            fileIndex: 0,
            uploading: 0
        }
    },
    methods: {
        onChange(evt) {
            var files = evt.target.files || evt.dataTransfer.files;
            for (file of files) {
                if (!this.fileInList(this.files, file)) {
                    this.files.push({
                                     'file': file,
                                     'index': this.fileIndex++,
                                     'state': 'Ready'
                                    });
                }
            }
            document.getElementById('single-file').value = '';
        },
        fileInList(files, file) {
            for (var i = 0; i < files.length; i++) {
                if (files[i].file.name == file.name) {
                    return true;
                }
            }
            return false;
        },
        removeFile(index) {
            for (var i = 0; i < this.files.length; i++) {
                if (this.files[i].index == index) {
                    this.files.splice(i, 1);
                    break;
                }
            }
        },
        uploadFiles() {
            for (var i = 0; i < this.files.length; i++) {
                this.uploading++;
                this.files[i].state = 'Uploading...';
                let req = new XMLHttpRequest();
                let formData = new FormData();
                formData.append('fileToUpload', this.files[i].file);
                formData.append('folder', 'New Images');
                let index = this.files[i].index;
                req.upload.addEventListener("load", function () {
                    this.files[index].state = 'Complete';
                    this.uploading--;
                    if (this.uploading == 0)
                    {
                        this.files = [];
                    }
                }.bind(this));
                req.open('POST', '/upload');
                req.send(formData);
            }
        }
    }
})