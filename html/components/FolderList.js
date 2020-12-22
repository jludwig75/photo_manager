app.component('folder-list', {
    template:
    /*html*/
`
    <div class="menu-title">
        <span class="component-title folder-info-item">
            Folders
        </span>
        <span class="folder-info-item" style="float: right">
            <button v-on:click="refreshFolderList">Refresh</button>
        </span>
    </div>
    <ul>
        <li v-for="folder in folderList" v-on:click="onClickFolder(folder.name)">
            <div class="folder-li">
                <div :class="{ selected: selectedFolderName == folder.name }">
                    <img width="20" src="/folder.png" v-on:click="onClickFolder(folder.name)">
                    {{ folder.name }}
                </div>
            </div>
        </li>
    </ul>
`,
    data() {
        return {
            folderList: [],
            selectedFolderName: null
        }
    },
    props: {
        override_folder_selection: {
            type: String,
            required: false
        }
    },
    methods: {
        updateFolderList(folderList) {
            for (const folderName of folderList) {
                this.folderList.push({'name': folderName})
            }
            if (folderList.length > 0 && this.selectedFolderName == null && this.override_folder_selection == null) {
                this.onClickFolder(folderList[0]);
            }
            else if (this.override_folder_selection != null && this.inFolderList(this.override_folder_selection)) {
                if (this.override_folder_selection == null) {
                    this.onClickFolder(folderList[0]);
                } else {
                    this.selectedFolderName = this.override_folder_selection;
                }
            }
        },
        onClickFolder(folderName) {
            this.selectedFolderName = folderName;
            this.$emit('folder-selected', folderName)
        },
        inFolderList(folderName) {
            for (folder of this.folderList) {
                if (folder.name == folderName) {
                    return true;
                }
            }
            return false;
        },
        refreshFolderList() {
            this.folderList = [];
            axios.
                get('/folders/').
                then(response => this.updateFolderList(response.data)).
                catch(error => console.log('Failed to get image list: ' + error));
        }
    },
    mounted() {
        this.refreshFolderList();
    }
})