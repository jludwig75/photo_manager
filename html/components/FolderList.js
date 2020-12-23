app.component('folder-list', {
    template:
    /*html*/
`
    <div class="folder-info">
        <div class="folder-info-content" style="padding-left: 0">
            <span class="folder-info-item component-title">
                Folders
            </span>
            <span class="folder-info-item" style="float: right">
                <button v-on:click="refreshFolderList">Refresh</button>
            </span>
        </div>
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
            selectedFolderName: null,
            timer: null
        }
    },
    props: {
        override_folder_selection: {
            type: String,
            required: false
        }
    },
    methods: {
        nameInFolderList(folderName) {
            for (const folder of this.folderList) {
                if (folderName == folder.name) {
                    return true;
                }
            }
            return false;
        },
        updateFolderList(folderList) {
            for (const folderName of folderList) {
                if (!this.nameInFolderList(folderName)) {
                    this.folderList.push({'name': folderName});
                }
            }
            var i = this.folderList.length;
            while(i--) {
                var folderName = this.folderList[i].name;
                if (!folderList.includes(folderName)) {
                    this.folderList.splice(i, 1);
                }
            }
            if (folderList.length > 0 && this.selectedFolderName == null && this.override_folder_selection == null) {
                console.log('Selecting first folder in list');
                this.onClickFolder(folderList[0]);
            }
            else if (this.override_folder_selection != null && this.inFolderList(this.override_folder_selection)) {
                if (this.override_folder_selection == null) {
                    console.log('Selecting first folder in list');
                    this.onClickFolder(folderList[0]);
                } else {
                    console.log('Selecting overriding selected folder');
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
            console.log("Refreshing folder list");
            axios.
                get('/folders/').
                then(response => this.updateFolderList(response.data)).
                catch(error => console.log('Failed to get image list: ' + error));
        }
    },
    beforeDestroy () {
        clearInterval(this.timer);
    },
    mounted() {
        this.refreshFolderList();
        this.timer = setInterval(() => {
            this.refreshFolderList();
        }, 60000);  // 1 minute
    }
})