import { shallowMount } from '@vue/test-utils';
import Identity from '@/components/Identity.vue';
import MockUrls from '../mockUrls';

window.Urls = MockUrls;

describe('Identity.vue', () => {
  let context;

  beforeEach(() => {
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
    const wrapper = shallowMount(Identity, { propsData, mocks });
    context = {
      $emit,
      $http,
      identity,
      wrapper,
    };
  });

  test('updateIdentity', () => {
    const { wrapper, $http, identity } = context;
    wrapper.vm.updateIdentity();

    expect($http.put).toBeCalledWith('/api/identities/1/', identity);
  });

  test('deleteIdentity', () => {
    const { wrapper, $emit, identity } = context;
    wrapper.vm.deleteIdentity();

    expect($emit).toBeCalledWith('deleteIdentity', identity);
  });
});
