app.component('image-details', {
    template:
    /*html*/
`
<div class="image-detail-header">
    <span v-if="current_image != null">
        Properties of {{ current_image.name }}:
    </span>
</div>
<div class="image-detail" v-for="detail in getDetailsList(current_image)">
    <div class="image-detail-name">
        {{ detail.name }}
    </div>
    <div class="image-detail-value">
        <span v-if="current_image != null">
            <span v-if="detail.locationLink != null"><a :href="detail.locationLink" target="_blank">{{ detail.value }}</a></span>
            <span v-else>{{ detail.value }}</span>
        </span>
    </div>
</div>
`,
    props: {
        current_image: {
            required: true
        }
    },
    methods: {
        compareObjects(object1, object2, key) {
            const obj1 = object1[key].toUpperCase()
            const obj2 = object2[key].toUpperCase()
          
            if (obj1 < obj2) {
              return -1
            }
            if (obj1 > obj2) {
              return 1
            }
            return 0
        },
        getDetailsList(image) {
            var detailsList = [];
            var imageLocation = null;
            var imageSize = null;
            for (var key in image) {
                if (!image.hasOwnProperty(key)) {
                    continue;
                }
                compareKey = key.toLocaleLowerCase();
                if (['name', 'index', 'link', 'thumbnail', 'thumbnailpath', 'format_mimetype'].includes(compareKey)) {
                    continue;
                }
                value = image[key];
                if (value instanceof Date) {
                    value = value.toLocaleDateString('en-US') + ', ' + value.toLocaleTimeString('en-US')
                }
                if (compareKey.includes('size') && Number.isFinite(value)) {
                    value = this.sizeString(value);
                }
                newKey = key.replace(/_bytes/g, '')
                if (key.toUpperCase().includes('LOCATION')) {
                    imageLocation = {
                                'name': this.formatKeyName(newKey),
                                'value': value,
                                'locationLink': 'https://www.google.com/maps/place/' + value
                               };
                } else if (key == 'size_bytes') {
                    imageSize = {
                                    'name': this.formatKeyName(newKey),
                                    'value': value,
                                    'locationLink': null
                                };
                }
                else {
                    detailsList.push({
                                        'name': this.formatKeyName(newKey),
                                        'value': value,
                                        'locationLink': null
                                    });
                }
            }
            detailsList.sort((book1, book2) => {
                return this.compareObjects(book1, book2, 'name')
            });
            if (imageLocation != null) {
                detailsList.unshift(imageLocation);
            }
            if (imageSize != null) {
                detailsList.unshift(imageSize);
            }
            return detailsList;
        },
        unCamelCase(str) {
            function isUpperCase(c) {
                if (c == c.toLocaleLowerCase()) {
                    return false;
                }
                return c == c.toUpperCase();
            };
            function lastChar(str) {
                if (str.length == 0) {
                    return '';
                }
                return str.charAt(str.length-1);
            }
            var newString = '';
            lastCharUpperCase = true;
            for (i = 0; i < str.length; i++) {
                c = str.charAt(i);
                if (isUpperCase(c) && !lastCharUpperCase && lastChar(newString) != ' ' && newString.length > 0) {
                    newString = newString.concat(' ');
                }
                lastCharUpperCase = isUpperCase(c);
                if (newString.length > 0 && lastChar(newString) == ' ' && i == str.length - 1 && !isUpperCase(str.charAt(i+1))) {
                    c = c.toLocaleLowerCase();
                }
                newString = newString.concat(c);
            }
            return newString;
        },
        formatKeyName(name) {
            name = name.replace(/_/g, ' ')
            name = name.charAt(0).toUpperCase() + name.slice(1);
            return this.unCamelCase(name);
        },
        getDisplayPrecision(number) {
            if (number < 10) {
                return 2;
            }
            if (number < 100) {
                return 1;
            }
            return 0;
        },
        sizeString(sizeBytes) {
            if (sizeBytes < 1024) {
                return sizeBytes + ' bytes';
            }
            sizeBytes /= 1024.0;
            if (sizeBytes < 1024) {
                return sizeBytes.toFixed(this.getDisplayPrecision(sizeBytes)) + '  KB';
            }
            sizeBytes /= 1024.0;
            return sizeBytes.toFixed(this.getDisplayPrecision(sizeBytes)) + ' MB';
        }
    }
})