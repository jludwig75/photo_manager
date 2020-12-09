app.component('folder-list', {
    template:
    /*html*/
`
    <div class="menu-title">
        <div class="component-title">
            Folders
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
            selectedFolderName: null
        }
    },
    methods: {
        updateFolderList(folderList) {
            if (folderList.length > 0 && this.selectedFolderName == null) {
                this.onClickFolder(folderList[0]);
            }
            for (const folderName of folderList) {
                this.folderList.push({'name': folderName})
            }
        },
        onClickFolder(folderName) {
            this.selectedFolderName = folderName;
            this.$emit('folder-selected', folderName)
        }
    },
    mounted() {
        axios.
            get('/folders/').
            then(response => this.updateFolderList(response.data)).
            catch(error => console.log('Failed to get image list: ' + error));
    }
})