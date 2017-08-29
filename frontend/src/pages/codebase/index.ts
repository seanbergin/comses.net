import EditCodebase from './edit'

function extractUrlParams(pathname: string) {
    let match = pathname.match(/\/codebases\/([0-9]+)\/edit\//);
    if (match !== null) {
        return { identifier: match[1] };
    }
    return { identifier: null }
}

new EditCodebase({ propsData: extractUrlParams(window.location.pathname)}).$mount('#app');