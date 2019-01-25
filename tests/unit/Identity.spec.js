import { shallowMount } from '@vue/test-utils';
import Identity from '@/components/Identity.vue';
import MockUrls from '../mockUrls';

window.Urls = MockUrls;

describe('Identity.vue', () => {
  const setup = options => {
    const $emit = jest.fn();
    const $http = {
      put: jest.fn(),
    };
    const mocks = {
      $emit,
      $http,
    };
    const identity = {
      id: 1,
      name: 'Test',
      url: 'https://example.com/',
    };
    const propsData = {
      identity,
      disabled: false,
    };
    const mountOptions = {
      propsData,
      mocks,
      ...options,
    };
    const wrapper = shallowMount(Identity, mountOptions);
    return {
      $emit,
      $http,
      identity,
      wrapper,
    };
  };

  test('update', () => {
    const { wrapper, $http, identity } = setup();
    wrapper.vm.update();

    expect($http.put).toBeCalledWith('/api/identities/1/', identity);
  });

  test('destroy', () => {
    const { wrapper, $emit, identity } = setup();
    wrapper.vm.destroy();

    expect($emit).toBeCalledWith('destroy', identity);
  });
});
