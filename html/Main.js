const app = Vue.createApp({
    data() {
        return {
            currentFolderName: null,
            currentImage: null
        }
    },
    methods: {
        updateSelectedFolder(selectedFolderName) {
            this.currentFolderName = selectedFolderName;
        },
        updateSelectedImage(selectedImage) {
            this.currentImage = selectedImage;
        }
    },
    computed: {
        current_folder_name() {
            return this.currentFolderName;
        },
        current_image() {
            return this.currentImage;
        }
    }
})
