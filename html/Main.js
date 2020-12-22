const app = Vue.createApp({
    data() {
        return {
            currentFolderName: null,
            currentImage: null,
            upload_dialog_mounts: 0,
            folder_list_updates: 0,
            folder_info_updates: 0,
            image_list_updates: 0,
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
            this.refreshFolderList();
            this.refreshFolderInfo();
        },
        showUploadDialog() {
            this.upload_dialog_mounts++;
            $('#upload-dialog').dialog({width: 800, height: 600});
            $('#userSelectedFolderName').focus();
        },
        onFolderDeleted() {
            this.override_folder_selection = null;
            this.currentFolderName = null;
            this.refreshFolderList();
        },
        refreshFolderList() {
            this.folder_list_updates++;
        },
        onImageDeleted() {
            this.currentImage = null;
            this.refreshFolderInfo();
        },
        refreshFolderInfo() {
            this.folder_info_updates++;
        },
        refreshCurrentFolder() {
            this.image_list_updates++;
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
