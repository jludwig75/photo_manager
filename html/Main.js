const app = Vue.createApp({
    data() {
        return {
            currentFolderName: null,
            currentImageLink: null
        }
    },
    methods: {
        updateSelectedFolder(selectedFolderName) {
            this.currentFolderName = selectedFolderName;
        },
        updateSelectedImage(selectedImageName) {
            this.currentImageLink = selectedImageName;
        }
    },
    computed: {
        current_folder_name() {
            return this.currentFolderName;
        },
        current_image_link() {
            return this.currentImageLink;
        }
    }
})
