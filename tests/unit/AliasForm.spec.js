import { shallowMount } from '@vue/test-utils';
import AliasForm from '@/components/AliasForm.vue';
import MockUrls from '../mockUrls';

jest.mock('axios');
window.Urls = MockUrls;

describe('AliasForm.vue', () => {
  const setup = options => {
    const aliases = [
      {
        id: 1,
        name: 'Test 1',
      },
      {
        id: 2,
        name: 'Test 2',
      },
    ];
    const userInSearch = false;
    const mockGet = url =>
      url.indexOf('profile') !== -1
        ? Promise.resolve({ data: { search_enabled: false } })
        : Promise.resolve({ data: aliases });
    const $http = {
      post: jest.fn().mockReturnValue(
        Promise.resolve({
          data: {
            id: 3,
            name: '',
          },
        }),
      ),
      patch: jest.fn().mockResolvedValue(Promise.resolve()),
      get: jest.fn(mockGet),
      delete: jest.fn().mockResolvedValue(Promise.resolve()),
    };
    const mocks = {
      $http,
    };
    const data = {
      aliases,
      userInSearch,
      draggingInProgress: false,
      runningRequests: 0,
    };
    const mountOptions = {
      mocks,
      data: () => data,
      ...options,
    };
    const wrapper = shallowMount(AliasForm, mountOptions);
    return {
      $http,
      mocks,
      wrapper,
      data,
    };
  };

  test('reorder', () => {
    const { data, $http, wrapper } = setup();
    wrapper.setData(data);
    wrapper.vm.reorder();

    expect($http.post).toBeCalledWith('/api/aliases/reorder/', [1, 2]);
  });

  test('create/NewAlias', () => {
    const { data, $http, wrapper } = setup();
    wrapper.setData(data);
    wrapper.vm
      .create()
      .then(() => {
        expect($http.post).toBeCalledWith('/api/aliases/', {
          name: '',
        });
        return wrapper.vm.$nextTick();
      })
      .then(() => {
        expect(wrapper.vm.aliases).toContainEqual({
          id: 3,
          name: '',
          disabled: false,
        });
      });
  });

  test('changeUserSearchStatus', () => {
    const { data, $http, wrapper } = setup();
    wrapper.setData({ userInSearch: true, aliases: data.aliases });
    wrapper.vm.changeUserSearchStatus().then(() => {
      expect($http.patch).toBeCalledWith('/api/profile/', {
        search_enabled: true,
      });
    });
  });

  test('destroy/destroyAlias', () => {
    const { data, $http, wrapper } = setup();
    wrapper.setData(data);
    wrapper.vm
      .destroy(data.aliases[0])
      .then(() => {
        expect($http.delete).toBeCalledWith('/api/aliases/1/');
        return wrapper.vm.$nextTick();
      })
      .then(() => {
        expect(wrapper.vm.aliases).not.toContainEqual({
          id: 1,
          name: 'Test 1',
        });
      });
  });

  test('retrieveAliases', () => {
    const { data, $http, wrapper } = setup();
    wrapper.vm.retrieveAliases(data.aliases[0]);

    expect($http.get).toBeCalledWith('/api/aliases/');
  });

  test('startDrag', () => {
    const { wrapper } = setup();
    wrapper.vm.startDrag();
    expect(wrapper.vm.draggingInProgress).toBeTruthy();
  });

  test('endDrag', () => {
    const { wrapper } = setup();
    wrapper.vm.reorder = jest.fn();
    wrapper.vm.endDrag();
    expect(wrapper.vm.draggingInProgress).toBeFalsy();
    expect(wrapper.vm.reorder).toHaveBeenCalled();
  });

  describe('aliasMoved', () => {
    test('invalid', () => {
      const { wrapper } = setup();
      const event = {
        direction: 'up',
        index: 0,
      };
      wrapper.vm.reorder = jest.fn();
      wrapper.vm.aliasMoved(event);
      expect(wrapper.vm.reorder).not.toHaveBeenCalled();
    });

    test('validUp', () => {
      const { wrapper } = setup();
      const event = {
        direction: 'up',
        index: 1,
        handle: {
          focus: jest.fn(),
        },
        el: {
          addEventListener: jest.fn(),
          removeEventListener: jest.fn(),
          getBoundingClientRect: jest.fn(),
          scrollIntoView: jest.fn(),
        },
      };
      wrapper.vm.$nextTick = jest.fn().mockImplementation(cb => cb());
      wrapper.vm.reorder = jest.fn();
      wrapper.vm.aliasMoved(event);
      expect(wrapper.vm.reorder).toHaveBeenCalled();
    });

    test('validDown', () => {
      const { wrapper } = setup();
      const event = {
        direction: 'down',
        index: 0,
        handle: {
          focus: jest.fn(),
        },
        el: {
          addEventListener: jest.fn(),
          removeEventListener: jest.fn(),
          getBoundingClientRect: jest.fn(),
          scrollIntoView: jest.fn(),
        },
      };
      wrapper.vm.$nextTick = jest.fn().mockImplementation(cb => cb());
      wrapper.vm.reorder = jest.fn();
      wrapper.vm.aliasMoved(event);
      expect(wrapper.vm.reorder).toHaveBeenCalled();
    });

    test('scroll events', () => {
      let transitionstart;
      let transitionend;
      const { wrapper } = setup();
      window.innerHeight = 5;
      window.requestAnimationFrame = jest.fn();
      const event = {
        direction: 'up',
        index: 1,
        handle: {
          focus: jest.fn(),
        },
        el: {
          addEventListener: (evt, cb) => {
            switch (evt) {
              case 'transitionstart':
                transitionstart = cb;
                break;
              case 'transitionend':
                transitionend = cb;
                break;
            }
          },
          removeEventListener: jest.fn(),
          getBoundingClientRect: jest.fn().mockImplementation(() => ({
            top: 1,
            bottom: 10,
          })),
          scrollIntoView: jest.fn(),
        },
      };
      wrapper.vm.$nextTick = jest.fn().mockImplementation(cb => cb());
      wrapper.vm.reorder = jest.fn();
      wrapper.vm.aliasMoved(event);

      transitionstart();
      expect(event.el.scrollIntoView).toHaveBeenCalledWith(false);

      event.el.getBoundingClientRect = jest.fn().mockImplementation(() => ({
        top: -1,
        bottom: 1,
      }));
      event.el.scrollIntoView.mockClear();
      transitionstart();
      expect(event.el.scrollIntoView).toHaveBeenCalledWith(true);

      event.el.getBoundingClientRect = jest.fn().mockImplementation(() => ({
        top: 1,
        bottom: 1,
      }));
      event.el.scrollIntoView.mockClear();
      transitionstart();
      expect(event.el.scrollIntoView).not.toHaveBeenCalled();

      transitionend();
      expect(event.el.removeEventListener).toHaveBeenCalled();
    });
  });
});
