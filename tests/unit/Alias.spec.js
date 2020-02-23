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

  describe('rearrangeSelf', () => {
    test('emits up', async () => {
      const { wrapper, $emit } = setup();
      await wrapper
        .find({ ref: 'rearrangeHandle' })
        .trigger('keydown', { keyCode: 38 });
      expect($emit).toHaveBeenCalledWith('moved', {
        index: 1,
        handle: wrapper.vm.$refs.rearrangeHandle,
        el: wrapper.vm.$el,
        direction: 'up',
      });
    });

    test('emits down', async () => {
      const { wrapper, $emit } = setup();
      await wrapper
        .find({ ref: 'rearrangeHandle' })
        .trigger('keydown', { keyCode: 40 });
      expect($emit).toHaveBeenCalledWith('moved', {
        index: 1,
        handle: wrapper.vm.$refs.rearrangeHandle,
        el: wrapper.vm.$el,
        direction: 'down',
      });
    });

    test('ignores anything else', async () => {
      const { wrapper, $emit } = setup();
      await wrapper
        .find({ ref: 'rearrangeHandle' })
        .trigger('keydown', { keyCode: 37 });
      expect($emit).not.toHaveBeenCalled();
    });
  });
});
