import { shallowMount } from '@vue/test-utils';
import AddButton from '@/components/AddButton.vue';
import MockUrls from '../mockUrls';

jest.mock('axios');
window.Urls = MockUrls;

describe('AddButton.vue', () => {
  test('Emits create on click', () => {
    const $emit = jest.fn();
    const wrapper = shallowMount(AddButton, { mocks: { $emit } });
    wrapper.vm.create();

    expect($emit).toBeCalledWith('create');
  });
});
