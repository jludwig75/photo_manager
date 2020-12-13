app.component('image-upload', {
    template:
    /*html*/
`
<div class="upload-dialog-item">
    <form>
        <fieldset>
            <legend class="upload-title">Select Upload Folder</legend>
            <div clas="upload-form-row">
                <input type="radio" id="user" v-model="folderChoice" value="user">
                <label for="user">Choose Folder Name</label>&nbsp;&nbsp;&nbsp;
                <input :disabled="folderChoice != 'user'" type="text" id="userSelectedFolderName" v-model="userEnteredName">
            </div>
            <div class="upload-form-row">
                <input type="radio" id="existing" v-model="folderChoice" value="existing">
                <label for="existing">Select Folder</label>&nbsp;&nbsp;&nbsp;
                <select :disabled="folderChoice != 'existing'" v-model="folderName">
                    <option :value="folderName">{{ folderName }}&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(New Folder)</option>
                    <option v-for="folder in folderList" :value="folder">{{ folder }}</option>
                </select>
            </div>
        </fieldset>
    </form>
</div>
<div class="upload-dialog-item" id="form-wrapper">
    <div class="upload-dialog-header-item">
        <form action="upload" enctype="multipart/form-data" @submit.prevent="onSubmit">
            <input id="single-file" type="file" name="files" multiple v-on:change="onChange"/><br />
            <label class="label-button" id="single-file-label" for="single-file">Add Files</label>
        </form>
    </div>
    <div class="upload-dialog-header-item">
        <button :disabled="files.length == 0 || this.filesToUpload > 0" v-on:click="clearList">Clear List</button>
    </div>
</div>
<div class="upload-dialog-item" id="upload-file-list">
    <ul>
        <li v-for="file in files" :key="file.index">
            <div class="upload-file-list-item">
                <button v-on:click="removeFile(file.index)">X</button>
            </div>
            <div class="upload-file-list-item upload-file-list-file-name">
                {{ file.file.name }}
            </div>
            <div class="upload-file-list-item upload-file-list-state">
                {{ file.state }}
            </div>
        </li>
    </ul>
</div>
<div class="upload-dialog-item">
    <div>
        <button :disabled="files.length == 0 || this.filesToUpload > 0" v-on:click="onUploadFiles">Upload Files</button>
    </div>
</div>
`,
    data() {
        return {
            files: [],
            fileIndex: 0,
            uploading: 0,
            filesToUpload: 0,
            folderName: null,
            suggestedFolderName: null,
            folderList: [],
            folderChoice: 'user',
            userEnteredName: ''
        }
    },
    props: {
        upload_dialog_mounts: {
            required: true
        }
    },
    methods: {
        updateFolderList(folderList) {
            for (const folderName of folderList) {
                this.folderList.push(folderName)
            }
        },
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
        sleep(ms) {
            return new Promise(resolve => setTimeout(resolve, ms));
        },
        onUploadFiles() {
            this.resetFilesNotYetUploaded();
            this.filesToUpload = this.files.length;
            this.uploadFiles();
        },
        uploadFiles() {
            console.log('uploadFiles ' + this.files.length + ':');
            if (this.folderChoice == 'user') {
                if (this.userEnteredName == '') {
                    // TODO: Find a way to put a red start on the missing field.
                    alert('You must specify a new folder name.');
                    return;
                }
                this.folderName = this.userEnteredName;
            }
            for (var i = 0; i < this.files.length; i++) {
                if (this.uploading >= 4) {
                    console.log(this.uploading + ' files currently uploading. Setting timeout and returning');
                    setTimeout(() => { this.uploadFiles(); }, 100);
                    return;
                }
                if (this.files[i].state == 'Ready') {
                    this.uploading++;
                    console.log('Uploading file ' + i + ':' + this.files[i].file.name + ' ' + this.uploading + ' files uploading');
                    this.files[i].state = 'Uploading...';
                    let req = new XMLHttpRequest();
                    let formData = new FormData();
                    formData.append('fileToUpload', this.files[i].file);
                    formData.append('folder', this.folderName);
                    let index = i;
                    req.addEventListener("load", function (evt) {
                        this.handleUploadCompletion(index, evt);
                    }.bind(this));
                    req.addEventListener("error", function (evt) {
                        this.handleUploadCompletion(index, evt, true);
                    }.bind(this));
                    req.addEventListener("abort", function (evt) {
                        this.handleUploadCompletion(index, evt, true);
                    }.bind(this));
                    req.open('POST', '/upload');
                    var ret = req.send(formData);
                    console.log('Sent upload post for file ' + i);
                }
            }
        },
        handleUploadCompletion(index, evt, failed=false) {
            if (failed) {
                this.files[index].state = 'Failed';
            } else {
                if (evt.currentTarget.status < 200 || evt.currentTarget.status >= 300) {
                    this.files[index].state = 'Failed';
                    if (evt.currentTarget.status == 409) {
                        this.files[index].state += ' - Image exists'
                    }
                } else {
                    this.files[index].state = 'Complete';
                }
            }
            this.filesToUpload--;
            this.uploading--;
            console.log('File ' + index + ':' + this.files[index].file.name + ' uploaded ' + this.uploading + ' files uploading');
            if (this.filesToUpload == 0)
            {
                this.clearCompletedFiles();
                this.$emit('upload-complete', this.folderName);
            }
        },
        clearCompletedFiles() {
            for (var i = 0; i < this.files.length; ) {
                if (this.files[i].state == 'Complete') {
                    this.files.splice(i, 1);
                } else {
                    i++;
                }
            }

            if (this.files.length == 0) {
                $( "#upload-dialog" ).dialog("close");
            }
        },
        resetFilesNotYetUploaded() {
            for (var i = 0; i < this.files.length; ) {
                if (this.files[i].state == 'Complete') {
                    this.files.splice(i, 1);
                } else {
                    this.files[i].state = 'Ready';
                    i++;
                }
            }
        },
        clearList() {
            this.files = [];
        },
        updateFolderName(folderName) {
            this.folderName = folderName;
            this.suggestedFolderName = folderName;
        }
    },
    mounted() {
        this.folderList = [];
        axios.
            get('/folders/').
            then(response => this.updateFolderList(response.data)).
            catch(error => console.log('Failed to get image list: ' + error));
        axios.
            get('/folders/suggest_folder_name').
                then(response => this.updateFolderName(response.data)).
                catch(error => console.log('Failed to suggested folder name: ' + error));
    }
})