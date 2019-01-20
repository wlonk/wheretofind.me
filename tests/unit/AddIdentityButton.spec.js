import { shallowMount } from '@vue/test-utils';
import AddIdentityButton from '@/components/AddIdentityButton.vue';
import MockUrls from '../mockUrls';

jest.mock('axios');
window.Urls = MockUrls;

describe('AddIdentityButton.vue', () => {
  test('Emits createIdentity on click', () => {
    const $emit = jest.fn();
    const wrapper = shallowMount(AddIdentityButton, { mocks: { $emit } });
    wrapper.vm.createIdentity();

    expect($emit).toBeCalledWith('createIdentity');
  });
});
