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
      tag: '',
      quality: 2,
      icon: 'fas fa-link',
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

  test('toggleExpanded', () => {
    const { wrapper } = setup();
    wrapper.vm.toggleExpanded();

    expect(wrapper.vm.expandExtras).toBeTruthy();
  });

  test('guessIcon', () => {
    const { wrapper } = setup({
      propsData: {
        identity: {
          id: 1,
          name: 'Test',
          url: 'https://mastodon/',
          tag: '',
          quality: 2,
          icon: 'fas fa-link',
        },
        disabled: false,
      },
    });
    wrapper.vm.guessIcon();

    expect(wrapper.vm.identity.icon).toEqual('fab fa-mastodon');
  });

  test('updateUrl', () => {
    const { wrapper } = setup();
    wrapper.vm.guessIcon = jest.fn();
    wrapper.vm.update = jest.fn();
    wrapper.vm.updateUrl();

    expect(wrapper.vm.guessIcon).toBeCalled();
    expect(wrapper.vm.update).toBeCalled();
  });

  describe('qualityPreview', () => {
    test.each([[0, 'low'], [1, 'mid'], [2, 'high']])(
      'at %i',
      (quality, expected) => {
        const { wrapper } = setup({
          propsData: {
            identity: {
              id: 1,
              name: 'Test',
              url: 'https://example.com/',
              tag: '',
              quality,
              icon: 'fas fa-link',
            },
            disabled: false,
          },
        });
        const qualitySrc = wrapper.vm.qualityPreview;

        expect(qualitySrc).toEqual([`/static/images/quality-${expected}.png`]);
      },
    );
    test('at else', () => {
      const { wrapper } = setup({
        propsData: {
          identity: {
            id: 1,
            name: 'Test',
            url: 'https://example.com/',
            tag: '',
            quality: -1,
            icon: 'fas fa-link',
          },
          disabled: false,
        },
      });
      const qualityClasses = wrapper.vm.qualityPreview;

      expect(qualityClasses).toEqual([]);
    });
  });
});
