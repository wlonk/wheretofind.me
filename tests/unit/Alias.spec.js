import { shallowMount } from '@vue/test-utils';
import Alias from '@/components/Alias.vue';
import MockUrls from '../mockUrls';

window.Urls = MockUrls;

describe('Alias.vue', () => {
  const setup = options => {
    const $emit = jest.fn();
    const $http = {
      put: jest.fn(),
    };
    const mocks = {
      $emit,
      $http,
    };
    const alias = {
      id: 1,
      name: 'Test',
      url: 'https://example.com/',
    };
    const propsData = {
      alias,
      disabled: false,
      index: 1,
    };
    const defaults = {
      mocks,
      propsData,
    };
    const mountOptions = {
      ...defaults,
      ...options,
    };
    const wrapper = shallowMount(Alias, mountOptions);
    return {
      $emit,
      $http,
      alias,
      wrapper,
    };
  };

  test('update', () => {
    const { wrapper, $http, alias } = setup();
    wrapper.vm.update();

    expect($http.put).toBeCalledWith('/api/aliases/1/', alias);
  });

  test('destroy', () => {
    const { wrapper, $emit, alias } = setup();
    wrapper.vm.destroy();

    expect($emit).toBeCalledWith('destroy', alias);
  });
});
