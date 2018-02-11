import EditProfile, {schema} from './edit'
import {__BASIC_AUTH_USERNAME__} from "../../__config__/common"
import { expect } from 'chai'

describe('profile editing', () => {
    it('should allow updates', async () => {
        try {
            // FIXME: figure out how to refactor this without username from __config__/common.ts
            const vm = new EditProfile({ propsData: { pk: 3}}); 
            await vm.initializeForm();
            expect((<any>vm).given_name).to.equal('Test');
            expect((<any>vm).email).to.equal('a@b.com');

            (<any>vm).given_name = 'foo';
            await vm.createOrUpdate();
            await vm.initializeForm();
            expect((<any>vm).given_name).to.equal('foo');

            (<any>vm).state.given_name = 'Test';
            await vm.createOrUpdate();
        } catch(e) {
            if (e.response) {
                console.log(e.response);
            }
            throw e;
        }
    });
});
