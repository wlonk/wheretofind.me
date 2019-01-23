import { shallowMount } from '@vue/test-utils';
import AliasForm from '@/components/AliasForm.vue';
import MockUrls from '../mockUrls';

jest.mock('axios');
window.Urls = MockUrls;

describe('AliasForm.vue', () => {
  let context;

  beforeEach(() => {
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
    context = {
      $http,
      data: { aliases, userInSearch },
      mocks,
    };
  });

  test('reorder', () => {
    const { mocks, data, $http } = context;
    const wrapper = shallowMount(AliasForm, { mocks });
    wrapper.setData(data);
    wrapper.vm.reorder();

    expect($http.post).toBeCalledWith('/api/aliases/reorder/', [1, 2]);
  });

  test('create/NewAlias', () => {
    const { mocks, data, $http } = context;
    const wrapper = shallowMount(AliasForm, { mocks });
    wrapper.setData(data);
    wrapper.vm
      .create()
      .then(() => {
        expect($http.post).toBeCalledWith('/api/aliases/', {
          name: '',
        });
        return wrapper.vm.nextTick();
      })
      .then(() => {
        expect(wrapper.vm.aliases).toContain({
          id: 3,
          name: '',
        });
      });
  });

  test('changeUserSearchStatus', () => {
    const { mocks, data, $http } = context;
    const wrapper = shallowMount(AliasForm, { mocks });
    wrapper.setData({ userInSearch: true, aliases: data.aliases });
    wrapper.vm.changeUserSearchStatus().then(() => {
      expect($http.patch).toBeCalledWith('/api/profile/', {
        search_enabled: true,
      });
    });
  });

  test('destroy/destroyAlias', () => {
    const { mocks, data, $http } = context;
    const wrapper = shallowMount(AliasForm, { mocks });
    wrapper.setData(data);
    wrapper.vm.destroy(data.aliases[0]);

    expect($http.delete).toBeCalledWith('/api/aliases/1/');
    expect(wrapper.vm.aliases).not.toContain({
      id: 1,
      name: 'Test 1',
    });
  });

  test('retrieveAliases', () => {
    const { mocks, data, $http } = context;
    const wrapper = shallowMount(AliasForm, { mocks });
    wrapper.vm.retrieveAliases(data.aliases[0]);

    expect($http.get).toBeCalledWith('/api/aliases/');
  });
});
