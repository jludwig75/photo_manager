const app = Vue.createApp({
    data() {
        return {
            currentFolderName: null,
            currentImage: null,
            upload_dialog_mounts: 0,
            folder_list_updates: 0,
            override_folder_selection: null
        }
    },
    methods: {
        updateSelectedFolder(selectedFolderName) {
            this.currentFolderName = selectedFolderName;
        },
        updateSelectedImage(selectedImage) {
            this.currentImage = selectedImage;
        },
        onUploadComplete(folderName) {
            this.override_folder_selection = folderName;
            this.currentFolderName = folderName;
            this.folder_list_updates++;
        },
        showUploadDialog() {
            this.upload_dialog_mounts++;
            $('#upload-dialog').dialog({width: 800, height: 600});
            $('#userSelectedFolderName').focus();
        }
    },
    computed: {
        current_folder_name() {
            return this.currentFolderName;
        },
        current_image() {
            return this.currentImage;
        }
    },
    mounted() {
    }
})
