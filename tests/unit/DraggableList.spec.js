import { shallowMount } from '@vue/test-utils';
import DraggableList from '@/components/DraggableList.vue';
import MockUrls from '../mockUrls';

jest.mock('axios');
window.Urls = MockUrls;

describe('DraggableList.vue', () => {
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
      post: jest.fn().mockReturnValue(Promise.resolve({})),
      get: jest.fn().mockResolvedValue({ data }),
      delete: jest.fn().mockResolvedValue(Promise.resolve()),
    };
    const mocks = {
      $http,
    };
    const mountOptions = {
      mocks,
      propsData: {
        __underlyingListProp: [...data],
      },
      slots: {
        listItems:
          '<div class="draggable-item"><div class="card-control-icon rearrange-handle"></div></div>',
      },
      ...options,
    };
    const wrapper = shallowMount(DraggableList, mountOptions);
    return {
      wrapper,
      $http,
      data: { items: data },
      mocks,
    };
  };

  test('startDrag', () => {
    const { wrapper } = setup();
    wrapper.vm.startDrag();
    expect(wrapper.vm.draggingInProgress).toBeTruthy();
  });

  test('endDrag', () => {
    const { wrapper } = setup();
    wrapper.vm.endDrag();
    expect(wrapper.vm.draggingInProgress).toBeFalsy();
  });

  describe('itemMoved', () => {
    test('invalid', () => {
      const { wrapper } = setup();
      const event = {
        direction: 'up',
        index: 0,
      };
      wrapper.vm.itemMoved(event);
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
      wrapper.vm.itemMoved(event);
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
      wrapper.vm.itemMoved(event);
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
      wrapper.vm.itemMoved(event);

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
