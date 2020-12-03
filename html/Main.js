const app = Vue.createApp({
    data() {
        return {
            currentFolderName: null
        }
    },
    methods: {
        updateSelectedFolder(selectedFolderName) {
            this.currentFolderName = selectedFolderName;
        }
    },
    computed: {
        current_folder_name() {
            return this.currentFolderName;
        }
    }
})
