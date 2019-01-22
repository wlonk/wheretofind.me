import { shallowMount } from '@vue/test-utils';
import Alias from '@/components/Alias.vue';
import MockUrls from '../mockUrls';

window.Urls = MockUrls;

describe('Alias.vue', () => {
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
    const alias = {
      id: 1,
      name: 'Test',
      url: 'https://example.com/',
    };
    const propsData = {
      alias,
      disabled: false,
    };
    const wrapper = shallowMount(Alias, { propsData, mocks });
    context = {
      $emit,
      $http,
      alias,
      wrapper,
    };
  });

  test('update', () => {
    const { wrapper, $http, alias } = context;
    wrapper.vm.update();

    expect($http.put).toBeCalledWith('/api/aliases/1/', alias);
  });

  test('destroy', () => {
    const { wrapper, $emit, alias } = context;
    wrapper.vm.destroy();

    expect($emit).toBeCalledWith('destroy', alias);
  });
});
