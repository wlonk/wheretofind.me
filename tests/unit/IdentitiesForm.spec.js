import { shallowMount } from '@vue/test-utils';
import IdentitiesForm from '@/components/IdentitiesForm.vue';
import Identity from '@/components/Identity.vue';
import MockUrls from '../mockUrls';

jest.mock('axios');
window.Urls = MockUrls;

describe('IdentitiesForm.vue', () => {
  const setup = options => {
    const data = [
      {
        id: 1,
        name: 'Test 1',
        url: 'https://example.com/1',
      },
      {
        id: 2,
        name: 'Test 2',
        url: 'https://example.com/2',
      },
    ];
    const $http = {
      post: jest.fn().mockReturnValue(
        Promise.resolve({
          data: {
            id: 3,
            name: '',
            url: '',
          },
        }),
      ),
      get: jest.fn().mockResolvedValue({ data }),
      delete: jest.fn().mockResolvedValue(Promise.resolve()),
    };
    const mocks = {
      $http,
    };
    const mountOptions = {
      mocks,
      data: () => ({
        identities: [...data],
        draggingInProgress: false,
        runningRequests: 0,
      }),
      ...options,
    };
    const wrapper = shallowMount(IdentitiesForm, mountOptions);
    return {
      wrapper,
      $http,
      data: { identities: data },
      mocks,
    };
  };

  test('reorder/Identities', () => {
    const { wrapper, data, $http } = setup();
    wrapper.setData(data);
    wrapper.vm.reorder();

    expect($http.post).toBeCalledWith('/api/identities/reorder/', [1, 2]);
  });

  test('create/NewIdentity', () => {
    const { wrapper, data, $http } = setup();
    wrapper.setData(data);
    wrapper.vm
      .create()
      .then(() => {
        expect($http.post).toBeCalledWith('/api/identities/', {
          name: '',
          url: '',
        });
        return wrapper.vm.$nextTick();
      })
      .then(() => {
        expect(wrapper.vm.identities).toContainEqual({
          id: 3,
          name: '',
          url: '',
          disabled: false,
          quality: 2,
          icon: 'fas fa-link',
        });
      });
  });

  test('destroy/deleteIdentity', () => {
    const { wrapper, data, $http } = setup();
    wrapper.setData(data);
    wrapper.vm
      .destroy(data.identities[0])
      .then(() => {
        expect($http.delete).toBeCalledWith('/api/identities/1/');
        return wrapper.vm.$nextTick();
      })
      .then(() => {
        expect(wrapper.vm.identities).not.toContainEqual({
          id: 1,
          name: 'Test 1',
          url: 'https://example.com/1',
        });
      });
  });

  test('retrieveIdentities', () => {
    const { wrapper, data, $http } = setup();
    wrapper.vm.retrieveIdentities(data.identities[0]);

    expect($http.get).toBeCalledWith('/api/identities/');
  });

  test('runningRequests count is properly incremented and decremented', async () => {
    const { wrapper, data } = setup();
    wrapper.setData(data);
    await wrapper.vm.$nextTick(); // so that the child Identity components are created
    expect(wrapper.vm.allRequestsComplete).toBe(true);
    expect(wrapper.vm.runningRequests).toBe(0);
    const createReq = wrapper.vm.create();
    expect(wrapper.vm.allRequestsComplete).toBe(false);
    expect(wrapper.vm.runningRequests).toBe(1);
    const destroyReq = wrapper.vm.destroy(data.identities[0]);
    expect(wrapper.vm.allRequestsComplete).toBe(false);
    expect(wrapper.vm.runningRequests).toBe(2);
    const reorderReq = wrapper.vm.reorder();
    expect(wrapper.vm.allRequestsComplete).toBe(false);
    expect(wrapper.vm.runningRequests).toBe(3);
    const updateReq = Promise.resolve('~ update request response ~');
    wrapper.find(Identity).vm.$emit('request-started', updateReq);
    expect(wrapper.vm.allRequestsComplete).toBe(false);
    expect(wrapper.vm.runningRequests).toBe(4);
    await createReq;
    await destroyReq;
    await reorderReq;
    await updateReq;
    expect(wrapper.vm.allRequestsComplete).toBe(true);
    expect(wrapper.vm.runningRequests).toBe(0);
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

  describe('identityMoved', () => {
    test('invalid', () => {
      const { wrapper } = setup();
      const event = {
        direction: 'up',
        index: 0,
      };
      wrapper.vm.reorder = jest.fn();
      wrapper.vm.identityMoved(event);
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
      wrapper.vm.identityMoved(event);
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
      wrapper.vm.identityMoved(event);
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
      wrapper.vm.identityMoved(event);

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
